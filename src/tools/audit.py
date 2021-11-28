from datetime import datetime, timedelta
import os
import logging

import click
import pandas as pd


def process_export(csv_file, rel_params, thresh):
    # load in the data 
    logging.info('Processing {}'.format(csv_file))
    df = pd.read_csv(csv_file)
    df.drop(columns=['answer_type'], inplace=True)
    logging.info('Raw df shape {}'.format(df.shape))

    # clean (time treshold > skips > repeat + contradictory answers)
    df = df[df['answer_time'] >= thresh]
    df.dropna(subset=['answer'], inplace=True)
    # drop duplicates
    df = df.drop_duplicates(
        subset=["ObfuscatedUserId", 'answer', 'question_id'], keep='last')
    # Drop contradictory responses
    df = df.drop_duplicates(
        subset=["ObfuscatedUserId", 'question_id'], keep=False)
    logging.info('Clean df shape {}'.format(df.shape))

    # # optimize memory
    # for col in df.columns:
    #     if col != 'answer_time':
    #         df[col] = df[col].astype("category")
    
    # df_1 = df[df['question_id'].str.contains('dd02|dd06|dd12', regex=True)].index
    # df_2 = df[~df['question_id'].str.contains('dd02|dd06|dd12', regex=True)]

    # b1_list = df[df['question_id'].str.contains('dd02|dd06|dd12', regex=True)]\
    #           .loc[:, 'question_id'].unique()
    # import pdb
    # pdb.set_trace()
    df['batch1'] = df['question_id'].str.contains('dd02|dd06|dd12', regex=True)
    df['batch'] = df.apply(lambda x: 1 if x['batch1'] else 2, axis=1)
    df.drop(columns=['batch1'], inplace=True)

    return df

def get_report(df, rep, img_total):
    overview = {
        "Image Total": img_total,
        "Image Count": len(df['question_id'].unique()),
        "Responders Count": len(df['ObfuscatedUserId'].unique()),
        "Responses Count": df.shape[0],
        "% True": (df[df['answer'] == True].shape[0])/df.shape[0],
        "% False": (df[df['answer'] == False].shape[0])/df.shape[0],
        "Threshold": rep,
        "Proportion ans >= threshold": sum(df.value_counts('question_id') >= rep)\
            /img_total}

    return pd.DataFrame(overview, index=["Value"]).T

def get_chart_list(df, rep, b):
    s = df[df['batch'] == b].value_counts('question_id')
    df_ = s[(s < rep)].to_frame().reset_index()
    df_.drop_duplicates(subset=['question_id'], inplace=True)
    logging.info('List df length {}'.format(df_.shape[0]))
    return df_.loc[:,['question_id']]
    
def last_monday():
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday())
    return last_monday.strftime("%m%d")


@click.command()
@click.option(
    '--file_dir', '-d',
    type=str,
    required=True,
    help='Location of csv answer exports'
)
@click.option(
    '--rep',
    type=click.IntRange(min=1,clamp=True),
    default=50,
    show_default=True,
    help='Minimum number of replications'
)
@click.option(
    '--time_threshold', '-t',
    type=click.FloatRange(min=0,clamp=True),
    default=0.1,
    show_default=True,
    help='Answer time treshold. Answers below will be discarded.'
)
@click.option(
    '--report', '-r',
    is_flag=True,
    help='Gets progress report.'
)
@click.option(
    '--requeue_list', '-ls',
    is_flag=True,
    help='Outputs a txt file with charts to requeue based on supplied parameters.'
)
@click.option(
    '--batch', '-b',
    type=click.Choice(['1', '2']),
    default='1',
    show_default=True,
    help='Which batch to use for the requeue list'
)
@click.option(
    '--rel_params', '-p',
    type=list,
    default=['data'],
    help='Parameters used in parsing'
)
def main(**opts):
    TIMESTAMP = datetime.now().strftime('%Y%m%d')

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    
    # get files
    logging.info('Getting files from {}'.format(last_monday()))
    read_csv = os.path.join(
        opts['file_dir'], 'chart_readability_{}.csv'.format(last_monday()))
    trust_csv = os.path.join(
        opts['file_dir'], 'chart_trustworthiness_{}.csv'.format(last_monday()))
    # read_csv = os.path.join(opts['file_dir'], 'test_r.csv')
    # trust_csv = os.path.join(opts['file_dir'], 'test_t.csv')
    
    # process files
    logging.info('Processing files')
    
    data = {
        'Read': process_export(
            read_csv, opts['rel_params'], opts['time_threshold']),
        'Trust': process_export(
            trust_csv, opts['rel_params'], opts['time_threshold'])}

    # data['Trust']['B1'], data['Trust']['B2'] = process_export(
    #     trust_csv, opts['rel_params'], opts['time_threshold'])
    
    if opts['report']:
        img_counts = {1: 110592, 2: 75744}
        logging.info('Saving report to %s', os.getcwd())

        with pd.ExcelWriter(
            '{}_charts_experiment_report.xlsx'.format(TIMESTAMP)) as writer:
            for k, v in data.items():
                for i in [1,2]:
                    get_report(v[v['batch']==i], opts['rep'], img_counts[i])\
                    .to_excel(writer,sheet_name='{}-B{}'.format(k,i))
    
    if opts['requeue_list']:
        logging.info(
            'Saving requeue lists for batch %s to %s',
            opts['batch'], os.getcwd())
        for task in data.keys():
            list_df = get_chart_list(
                data[task], opts['rep'], int(opts['batch']))
            list_df.to_csv(
                '{}_rq_list_{}_B{}.txt'.format(TIMESTAMP, task, opts['batch']),
                index=False, header=False)


if __name__ == '__main__':
    main()