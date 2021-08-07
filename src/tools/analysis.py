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
            param = df_[k].dropna().astype(int)
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
            critical = stats.chi2.ppf(chi_p, dof)
            
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
                "Significant": abs(chi_stat) >= critical,
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