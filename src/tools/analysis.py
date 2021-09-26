from itertools import combinations

import dython
import pandas as pd
import numpy as np
from scipy import stats


def get_summary(df, user_col='ObfuscatedUserId', q_col='answer', ch_col='question_id', multi=False):
    """Table with Descriptive highlights

    Args:
        df: dataframe
        user_col (str, optional): column with user identifiers. Defaults to 'ObfuscatedUserId'.
        q_col (str, optional): column with answer identifiers. Defaults to 'answer'.
        ch_col (str, optional): column with chart identifiers. Defaults to 'question_id'.
        multi (bool, optional): if the answers are multiclass. Defaults to False.

    Returns:
        overview: summary dataframe
    """
    overview = {
        "RespondersCount": len(df[user_col].unique()),
        "ResponsesCount": df.shape[0],
        "ImageCount": len(df[ch_col].unique()),
        "AnsSkipCount": df[q_col].isna().sum()
    }
    if multi:
        overview["ProportionSkip"] = overview["AnsSkipCount"]/overview['ResponsesCount']
        for i in df[q_col].dropna().unique():
            overview["Ans{}Count".format(i)] = df[df[q_col] == i].shape[0]
            overview["Proportion{}".format(i)] = overview["Ans{}Count".format(i)]/overview['ResponsesCount']
    else:
        overview["AnsTrueCount"] = df[df[q_col] == True].shape[0]
        overview["AnsFalseCount"] = df[df[q_col] == False].shape[0]
        for i in ['True', 'False', 'Skip']:
            overview["Proportion{}".format(i)] = overview["Ans{}Count".format(i)]/overview['ResponsesCount']

    return pd.DataFrame(overview, index=["Value"]).T

def get_table_summary( 
    df_t, df_r, d1_name='Trustworthiness', d2_name='Readability',
    user_col='ObfuscatedUserId', q_col='answer', ch_col='question_id'
    ):
    """gives summary for two dataframes

    Args:
        df_t (DataFrame): DataFrame 1 (trustworthiness)
        df_r (DataFrame): DataFrame 2 (readability)
    """
    # get summary for table 1 & 2 
    df_t_sum = get_summary(df_t)
    df_r_sum = get_summary(df_r)

    # aggregate by image
    ratings_by_image = {
        d1_name: pd.crosstab(df_t[ch_col], df_t[q_col], dropna=False),
        d2_name: pd.crosstab(df_r[ch_col], df_r[q_col], dropna=False)
    }
    ratings_by_image[d1_name]['Total']= ratings_by_image[d1_name].sum(axis=1)
    ratings_by_image[d2_name]['Total']= ratings_by_image[d2_name].sum(axis=1)

    # aggregate by user
    ratings_by_user = {
        "trust": pd.crosstab(df_t[user_col], df_t[q_col], dropna=False),
        "read": pd.crosstab(df_r[user_col], df_r[q_col], dropna=False)
    }
    ratings_by_user[d1_name]['Total']= ratings_by_user[d1_name].sum(axis=1)
    ratings_by_user[d2_name]['Total']= ratings_by_user[d2_name].sum(axis=1)

    d = {d1_name: {}, d2_name: {}, 'Total': {}}

    # Image
    d[d1_name]['Images'] = df_t_sum.loc['ImageCount','Value']
    d[d2_name]['Images'] = df_r_sum.loc['ImageCount','Value']
    d['Total']['Images'] = d[d1_name]['Images'] + d[d2_name]['Images'] - len(np.intersect1d(df_t[ch_col].unique(),df_r[ch_col].unique()))

    # Unique contributors
    d[d1_name]['Contributors'] = df_t_sum.loc['RespondersCount','Value']
    d[d2_name]['Contributors'] = df_r_sum.loc['RespondersCount','Value']
    d['Total']['Contributors'] = d[d1_name]['Contributors'] + d[d2_name]['Contributors'] - len(np.intersect1d(df_t[user_col].unique(),df_r[user_col].unique()))

    # Answers
    d[d1_name]['Answers'] = df_t_sum.loc['ResponsesCount','Value']
    d[d2_name]['Answers'] = df_r_sum.loc['ResponsesCount','Value']
    d['Total']['Answers'] = d[d1_name]['Answers'] + d[d2_name]['Answers']

    # % yes
    d[d1_name]['% Yes'] = df_t_sum.loc['ProportionTrue','Value']
    d[d2_name]['% Yes'] = df_r_sum.loc['ProportionTrue','Value']

    # % no
    d[d1_name]['% No'] = df_t_sum.loc['ProportionFalse','Value']
    d[d2_name]['% No'] = df_r_sum.loc['ProportionFalse','Value']

    # % skip
    d[d1_name]['% Skip'] = df_t_sum.loc['ProportionSkip','Value']
    d[d2_name]['% Skip'] = df_r_sum.loc['ProportionSkip','Value']

    # Avg Answer per contributor
    d[d1_name]['Avg Ans/Contributor'] = ratings_by_user[d1_name]['Total'].mean()
    d[d2_name]['Avg Ans/Contributor'] = ratings_by_user[d2_name]['Total'].mean()

    # StDev Answer per contributor
    d[d1_name]['StDev Ans/Contributor'] = ratings_by_user[d1_name]['Total'].std()
    d[d2_name]['StDev Ans/Contributor'] = ratings_by_user[d2_name]['Total'].std()

    # Avg Answer per image
    d[d1_name]['Avg Ans/Image'] = ratings_by_image[d1_name]['Total'].mean()
    d[d2_name]['Avg Ans/Image'] = ratings_by_image[d2_name]['Total'].mean()

    # StDev Answer per image
    d[d1_name]['StDev Ans/Image'] = ratings_by_image[d1_name]['Total'].std()
    d[d2_name]['StDev Ans/Image'] = ratings_by_image[d2_name]['Total'].std()

    return pd.DataFrame(d)


def run_tests(df, target_col='answer', cols=['type', 'color', 'data'], prob=0.95):
    """
    Runs Chi-Square (two-tailed) and Kruskal-Wallis tests.
    Gets effect size coefficients (V, tau, rho) and uncertainty coefficient (U).

    Args:
        df ([dataframe]): dataframe
        target_col (str, optional): Column containing answer/response variable. Defaults to 'answer'.
        cols ([type], optional): Columns to apply the tests to. Defaults to ['type', 'color', 'data'].
        prob (float, optional): Probability to test at. Defaults to 0.95.

    Returns:
        [dataframe]: dataframe with results
    """
    non_ordinal = [
        'type', 'color', 'bar_orientation', 'font', 'legend_loc'
    ]

    if cols is None:
        cols = df.columns
        
    contingency_tables = {
      i: pd.crosstab(df[target_col], df[i]).values 
      for i in list(cols)
    }

    if 'error_bar' in cols:
        df['error_bar'] = df['error_bar'].replace('None', 0).replace('Line', 1).replace('Cap', 1)

    data = {}

    for k,v in {i: df[i].dropna().unique() for i in cols}.items():
        # chi-squared test
        chi_stat, chi_p, dof, expected  = stats.chi2_contingency(contingency_tables[k])
        critical = stats.chi2.ppf(prob, dof)

        # kruskal-wallis test
        try:
            k_args = [df[df[k] == j][target_col].dropna().astype(int) for j in v]
            k_stat, k_p = stats.kruskal(*k_args)
        except ValueError as e:
            print(e, "skipping {}".format(k))
            k_p = np.nan

        if k not in non_ordinal:
            df_ = df.dropna(subset=[target_col])
            param = df_[k].dropna().astype(float)
            ans = df_.loc[param.index,target_col].astype(int)

            # rank correlation
            kt_coeff, kt_p = stats.kendalltau(ans, param)
            pr_coeff, pr_p = stats.spearmanr(ans, param)
        else:
            kt_coeff, kt_p, pr_coeff, pr_p = np.nan, np.nan, np.nan, np.nan

        data[k] = {
          'Chi p-val': chi_p,
          'Chi significant': abs(chi_stat) >= critical, # two-tailed test
          'KW p-val': k_p,
          'KW significant': k_p <= 1-prob, # two-tailed test
          "Cramer's V": dython.nominal.cramers_v(df['answer'], df[k]),
          "Kendall's Tau": kt_coeff if k not in non_ordinal else np.nan,
          "Tau Significant": kt_p <= 1-prob if k not in non_ordinal else np.nan,
          "Spearman’s Rho": pr_coeff if k not in non_ordinal else np.nan,
          "Rho significant": pr_p <= 1-prob if k not in non_ordinal else np.nan,
          "Theil's U": dython.nominal.theils_u(df['answer'], df[k])
        }

    return pd.DataFrame(data).T


def adapted_fisher(df, target_col='answer', cols=None, prob=0.95, type_="Fisher", alternative='two-sided'):
    """
    Determines if answer is dependent on the parameter.
    If parameters are not binary, dependance if evaluated by each possible pair.

    Args:
        df ([dataframe]): dataframe
        target_col (str, optional): Column containing answer/response variable. Defaults to 'answer'.
        cols ([type], optional): Columns to apply the tests to. Defaults to None, which covers all.
        prob (float, optional): Probability to test at. Defaults to 0.95.
        alternative (str, optional): How to test H_1. Defaults to 'two-sided'.

    Returns:
        [dataframe]: dataframe with results
    """

    if cols is None:
        cols = df.columns

    contingency_tables = {
      "{}-{}".format(
          k, v_
          ): pd.crosstab(
              df[df[k].isin(list(v_))][target_col],
              df[df[k].isin(list(v_))][k]
            ).values for k,v in {
                j: list(
                    combinations(df[j].dropna().unique(),2)
                ) for j in cols}.items() for v_ in v
    }

    data = {}
    if type_== "Fisher":
        for k in contingency_tables.keys():
            oddsratio, pvalue = stats.fisher_exact(
                contingency_tables[k],
                alternative=alternative
            )
            data[k] = {
                "Significant": pvalue <= 1 - prob,
                "Yule's Q": (oddsratio-1)/(oddsratio+1),
                "Yule's Y":  (np.sqrt(oddsratio)-1)/(np.sqrt(oddsratio)+1),
                "OddsRatio": oddsratio,
                "P-value": pvalue,
                
            }
    if type_ == "Chi":
        non_ordinal = [
        'type', 'color', 'bar_orientation', 'font', 'legend_loc'
    ]
        for k in contingency_tables.keys():
            chi_stat, chi_p, dof, expected = stats.chi2_contingency(
                contingency_tables[k]
            )
            critical = stats.chi2.ppf(prob, dof)
            
            # kruskal-wallis test
            try:
                k_stat, k_p = stats.kruskal(*contingency_tables[k])
            except ValueError as e:
                print(e, "skipping {}".format(k))
                k_p = np.nan

            k_ = k.split("-")[0]

            if k_ not in non_ordinal:
                df_ = df.dropna(subset=[target_col])
                param = df_[k_].dropna().astype(int)
                ans = df_.loc[param.index,target_col].astype(int)

                # rank correlation
                kt_coeff, kt_p = stats.kendalltau(ans, param)
                pr_coeff, pr_p = stats.spearmanr(ans, param)
            else:
                kt_coeff, kt_p, pr_coeff, pr_p = np.nan, np.nan, np.nan, np.nan 
            data[k] = {
                "Chi Significant": abs(chi_stat) >= critical,
                "P-value": chi_p,
                'KW p-val': k_p,
                'KW significant': k_p <= 1-prob, # two-tailed test
                "Cramer's V": dython.nominal.cramers_v(df['answer'], df[k_]),
                "Kendall's Tau": kt_coeff if k_ not in non_ordinal else np.nan,
                "Tau Significant": kt_p <= 1-prob if k_ not in non_ordinal else np.nan,
                "Spearman’s Rho": pr_coeff if k_ not in non_ordinal else np.nan,
                "Rho significant": pr_p <= 1-prob if k_ not in non_ordinal else np.nan,
                "Theil's U": dython.nominal.theils_u(df['answer'], df[k_])

            }
    
    return pd.DataFrame(data).T