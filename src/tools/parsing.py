import numpy as np
import pandas as pd
import re

def parse_chart_name(dataframe, target_col, relevant_params=None, ans_source='crowdsource', ans_3=False):
    """Returns datafame with parsed parameters in columns
    Args:
        dataframe (Dataframe): Data in Pandas dataframe
        target_col (str): name of the column in dataframe that holds the chart names. Eg. 'question_id'.
        ans_source (str, optional): name of the platform. Defaults to crowdsource.
        relevant_params (list, optional): Choose which secondary (NOT type or color) parameters to include. 
                                          Choose from [
                                              "data", "source", "donut_hole", "grid", "wedge_explode",
                                              "rotation", "precision", "font", "font_size", "legend_loc",
                                              "error", "bar_width", "bar_spacing", "sample", "annotation_dist"
                                          ]
                                          Defaults to None, which includes all of them.
        ans_3 (bool, optional): Only implemented for Crowdsource output. Changes answers to a three-point scale. Defaults to False.

    Returns:
        Dataframe: Dataframe with parameters in separate columns
    """
    PARAM_MAP ={
        "data": r'(dd..)',
        "source": r'(sa..)',
        "donut_hole": r'(dh\d)',
        "grid": r'(gr..)',
        "wedge_explode": r'(we..)',
        "rotation": r'(ro...)',
        "precision": r'(pa..)',
        "font": r'(ft..)',
        "error": r'(e..a.)',
        "legend_loc": r'(ll..)',
        "bar_orientation": r'(bo.)',
        "bar_spacing": r'(bs...)',
        "bar_width": r'(bw.)',
        "sample": r'(sm.)',
        "font_size": r'(fs..)',
        "annotation_dist": r'(ad..)'
    }

    NUMERIC = [
        "data", "donut_hole", "wedge_explode", "rotation", "precision", "bar_spacing", "bar_width", "font_size", "annotation_dist"
    ]

    dataframe = dataframe.join(dataframe[target_col].str.split('-', expand=True).iloc[:,:2].rename(columns={0:"type", 1:"color"}))
    
    dataframe['type'].replace("PP", "Pie", inplace=True)
    dataframe['type'].replace("PD", "Donut", inplace=True)
    dataframe['type'].replace("PB", "Bar", inplace=True)

    for k,v in PARAM_MAP.items():
        if (not relevant_params or k in relevant_params):
            dataframe[k] = dataframe[target_col].str.extract(v, expand=True)
            if k != 'error':
                dataframe[k] = dataframe[k].str.replace(PARAM_MAP[k][1:3], "")
            if k in NUMERIC:
                dataframe[k] = pd.to_numeric(dataframe[k], errors='coerce')
                if k == 'precision':
                    dataframe["precision"].fillna(0, inplace=True)
                if k == 'bar_spacing':
                    dataframe["bar_spacing"] /= 1000
                if k == 'wedge_explode':
                    dataframe["wedge_explode"] /= 100
                for i in ['bar_width','annotation_dist', 'donut_hole']:
                    if i == k:
                        dataframe[i] /= 10
            if k == 'source':
                dataframe['source'].replace("no", False, inplace=True)
                dataframe['source'].replace(r"..", True, regex=True, inplace=True)
            if k == 'sample':
                dataframe['sample'].replace("0", False, inplace=True)
                dataframe['sample'].replace("1", True, inplace=True)
            if k == 'grid':
                dataframe['grid'].replace('00', False, inplace=True)
                dataframe['grid'].replace('0y', True, inplace=True)
            if k == 'bar_orientation':
                dataframe['bar_orientation'] = dataframe['bar_orientation'].str.upper()

    try:
        dataframe['error_bar'] = dataframe['error'].str.extract(r'(e..)', expand=True)
        dataframe['label'] = dataframe['error'].str.extract(r'(a.)', expand=True)

        for (i,j) in [
            ('e10','Line'),
            ('e11','Cap'),
            ('e00','None')
        ]:
            dataframe['error_bar'].replace(i, j, inplace=True)

        for (i,j) in [('a0', False),('a1', True)]:
            dataframe['label'].replace(i, j, inplace=True)

        # remove intermediary column
        dataframe.drop(columns=["error"], inplace=True)

    except KeyError:
        pass
    
    # convert mturk & prolific answers from str to bool/nan
    if ans_source.lower() != 'crowdsource':
        dataframe['answer'].replace('yes', True, inplace=True)
        dataframe['answer'].replace('no', False, inplace=True)
        dataframe['answer'].replace('skip', np.nan, inplace=True)

    # add 'skips' for 3-point answer scale
    if ans_3:
        # answers in the same column
        dataframe['answer'].fillna(value='Skip',  inplace=True)
        
    return dataframe

def parse_prolific(dataframe):
    """Parsing function to transform horizontal Prolific data output to
    Crowdsource-like verical output.

    Args:
        dataframe: DataFrame with Prolific data

    Raises:
        ValueError: when transformation dimentions are wrong

    Returns:
        dataframe: transformed dataframe
    """

    dataframe.drop(
        columns=[
            'attention_check_question','attention_check_answer'
        ]
    )

    imgs = dataframe.melt(
        id_vars=['session_date', 'prolific_id'],
        value_vars=[
            'image_1','image_2','image_3','image_4',
            'image_5','image_6','image_7','image_8',
            'image_9','image_10','image_11','image_12'
        ]
    )

    answers = dataframe.melt(
        id_vars=['session_date', 'prolific_id'],
        value_vars=[
            'image_1_answer','image_2_answer','image_3_answer','image_4_answer',
            'image_5_answer','image_6_answer','image_7_answer','image_8_answer',
            'image_9_answer','image_10_answer','image_11_answer','image_12_answer'
        ]
    )

    if not imgs.iloc[:, :-2].equals(answers.iloc[:, :-2]):
        raise ValueError("Images and answers do not line up.")

    dataframe = imgs.join(answers.iloc[:, -2:], rsuffix='_other')

    dataframe.drop(columns=['variable', 'variable_other'], inplace=True)
    dataframe.rename(
        columns={
            'value': 'question_id',
            'value_other': 'answer'
        },
        inplace=True
    )

    return dataframe

def parse_mturk(dataframe):
    pass

def parse_chart_name_neal(dataframe, target_col='question_id', answer_col=None):
    """Parsing function for Neal's naming scheme

    Args:
        dataframe: dataframe with experiment data
        target_col (str, optional): column with chart names to parse. Defaults to 'question_id'.
        answer_col (str, optional): column with answers. Defaults to None.

    Returns:
        dataframe: parsed dataframe
    """
    dataframe[target_col] = dataframe[target_col].str.replace(".png", "", regex=False)
    
    # data
    dataframe['data'] = dataframe.apply(
        lambda x: 2 if x[target_col][-1] == "2" else 1,
        axis=1
    )
    # type
    dataframe['type'] = dataframe.apply(
        lambda row: type_parse(row, target_col),
        axis=1
    )
    # source
    dataframe['source'] = dataframe.apply(
        lambda row: source_parse(row, target_col),
        axis=1
    )
    # trend_positive
    dataframe['trend_positive'] = dataframe.apply(
        lambda row: bool(re.search('^(((Line)|(Bar))((Group)|(Sing)))?S?P', row[target_col])),
        axis=1
    )
    # trend_strong
    dataframe['trend_strong'] = dataframe.apply(
        lambda row: bool(re.search('^(((Line)|(Bar))((Group)|(Sing)))?S?[PN]S', row[target_col])),
        axis=1
    )
    # title
    dataframe['title'] = dataframe.apply(
        lambda row: bool(re.search('^((Line|Bar)(Group|Sing))?S?[PN][SW]T', row[target_col])),
        axis=1
    )
    # grid
    dataframe['grid'] = dataframe.apply(
        lambda row: bool(re.search('^((Line|Bar)(Group|Sing))?S?[PN][SW][TN]G', row[target_col])),
        axis=1
    )
    # color
    dataframe['color'] = dataframe.apply(
        lambda row: color_parse(row, target_col),
        axis=1
    )
    # line of best fit
    dataframe['line'] = dataframe.apply(
        lambda row: line_bf(row, target_col),
        axis=1
    )
    # numeric answers
    if answer_col:
        dataframe[answer_col] = pd.to_numeric(dataframe[answer_col], errors='coerce')
   
    return dataframe

def type_parse(row, target_col):
    if bool(re.search('^BarGroup', row[target_col])):
        val = 'BarGroup'
    elif bool(re.search('^BarSing', row[target_col])):
        val = 'BarSing'
    elif bool(re.search('^LineGroup', row[target_col])):
        val = 'LineGroup'
    elif bool(re.search('^LineSing', row[target_col])):
        val = 'LineSing'
    else:
        val = 'Scatter'
    return val

def color_parse(row, target_col):
    if bool(re.search('B$', row[target_col])) or bool(re.search('B2$', row[target_col])):
        val = 'bnw'
    elif bool(re.search('C$', row[target_col])) or bool(re.search('C2$', row[target_col])):
        val = 'color'
    else:
        val = np.nan
    return val

def line_bf(row, target_col):
    if len(row[target_col]) == 6 or len(row[target_col]) == 7:
        if bool(re.search('L$', row[target_col])) or bool(re.search('L2$', row[target_col])):
            val = True
        else:
            val = False
    else:
        val = np.nan
    return val

def source_parse(row, target_col):
    if row['type'] == 'Scatter':
        if row[target_col][0] == 'S':
            val = True
        else:
            val = False
    else:
        val = bool(re.search('^((Line)|(Bar))((Group)|(Sing))S', row[target_col]))
    return val

def clean(df, target_col='question_id', answer_col='answer', user_col="ObfuscatedUserId", skip_alias=None):
    if skip_alias:
        df[answer_col].replace(skip_alias, np.nan, inplace=True)
    df.dropna(subset=[answer_col], inplace=True)
    df = df.drop_duplicates(subset=[user_col, answer_col, target_col], keep='last')
    # Drop contradictory responses
    # if there's more than one answer when grouped by user & answer, then there's yes and no 
    df = df.drop_duplicates(subset=[user_col, target_col], keep=False)
    return df