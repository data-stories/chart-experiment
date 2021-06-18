def parse_chart_name(dataframe, target_col, relevant_params=None, ans_3=False):
    """Only fully implemented for Crowdsource; should work with Prolific

    Args:
        dataframe (Dataframe): Data in Pandas dataframe
        target_col (str): name of the column in dataframe that holds the chart names. Eg. 'question_id'
        relevant_params (list, optional): Choose which secondary (NOT type, color, or data) parameters to include. Defaults to None, which includes all of them.
        ans_3 (bool, optional): Only implemented for Crowdsource output. Changes answers to a three-point scale. Defaults to False.

    Returns:
        Dataframe: Dataframe with parameters in separate columns
    """
    PARAM_MAP ={
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

    dataframe = dataframe.join(dataframe[target_col].str.split('-', expand=True).iloc[:,:3].rename(columns={0:"type", 1:"color", 2: "data"}))

    for k,v in PARAM_MAP.items():
        if (not relevant_params or k in relevant_params):
            dataframe[k] = dataframe[target_col].str.extract(v, expand=True)

    try:
        dataframe['error_bar'] = dataframe['error'].str.extract(r'(e..)',expand=True)
        dataframe['label'] = dataframe['error'].str.extract(r'(a.)',expand=True)

        for (i,j) in [
            ('e10','line'),
            ('e11','cap'),
            ('e00','none')
        ]:
            dataframe['error_bar'].replace(i, j, inplace=True)

        for (i,j) in [('a0', False),('a1', True)]:
            dataframe['label'].replace(i, j, inplace=True)
        
        # remove intermediary column
        dataframe.drop(columns=["error"], inplace=True)

    except KeyError:
        pass

    # add 'skips' for 3-point answer scale
    if ans_3:
        # answers in the same column
        dataframe[['answer']] = dataframe[['answer']].fillna(value='Skip')
        
    return dataframe