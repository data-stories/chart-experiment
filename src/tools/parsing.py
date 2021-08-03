import numpy as np
import pandas as pd

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
