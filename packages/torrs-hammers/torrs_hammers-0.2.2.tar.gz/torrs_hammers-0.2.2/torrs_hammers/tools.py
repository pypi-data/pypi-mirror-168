# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
import pandas as pd
from scipy import stats
import os, sys

def choose_multiple_values_in_column(df, colName, values):
    '''
    Return the dataframe (df) with selected string (values) in colName
    @param df: pandas dataframe
    @param colName: which column
    @param values: what are the values of intrest
    @return: dataframe (df) with selected string (values) in colName
    '''
    return df[df[colName].str.contains('|'.join(values))]

def sclmns(df, s, not_in=False):
    '''
    Return all the columns that (not) contain the names in s.
    :param df: pandas dataframe.
    :param s: string(s) the column(s) contains.
    :param not_in: all columns except the ones selected.
    :return: list of columns.
    '''
    clmns = []
    if not_in:
        # all_clmns = list(df.columns)
        all_clmns = df.columns
        for i in s:
            # all_clmns.remove(i)
            # all_clmns = [x for x in all_clmns if not x.__contains__(i)]
            all_clmns = all_clmns[~all_clmns.str.contains(i)]
        clmns = list(all_clmns)
        # clmns = all_clmns.copy()
    else:
        for i in s:
            clmns = clmns + list(df.columns[df.columns.str.contains(i)])
    return clmns

def calculate_corr_with_pvalues(df, method = 'pearsonr'):
    '''
    Calculate the correlation between the columns of dataframe and return values with stars.
    :param df: dataframe
    :param method: pearsonr/ spearman
    :return: pvalues, corr_with_stars
    '''
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')

    rho = df.corr()

    for r in df.columns:
        for c in df.columns:
            if method == 'pearsonr':
                pvalues[r][c] = round(stats.pearsonr(df[r], df[c])[1], 4)
            elif method == 'spearman':
                pvalues[r][c] = round(stats.spearmanr(df[r], df[c])[1], 4)
            elif method == 'reg':
                slope, intercept, rho[r][c], pvalues[r][c], std_err = stats.linregress(x=df[r],y= df[c])

    rho = rho.round(2)
    pval = pvalues
    # create three masks
    r1 = rho.applymap(lambda x: '{}*'.format(x))
    r2 = rho.applymap(lambda x: '{}**'.format(x))
    r3 = rho.applymap(lambda x: '{}***'.format(x))
    # apply them where appropriate
    rho = rho.mask(pval <= 0.05, r1)
    rho = rho.mask(pval <= 0.01, r2)
    rho = rho.mask(pval <= 0.001, r3)

    return pvalues, rho


def save_latex(data_path, df, fn, ix = True):
    '''
    Save dataframe with latex file
    :param data_path: were to open the .tex file
    :param df: pandas dataframe
    :param fn: filename
    :param ix: save index
    :return:
    '''
    with open(data_path + '%s.tex' %fn, 'w') as tf:
        if type(df) != pd.core.frame.DataFrame:
            df = pd.DataFrame(df)
        tf.write(df.to_latex(float_format=lambda x: '%.3f' % x, index=ix))
        df.to_csv(data_path + '%s.csv' % fn)


def ttest_or_mannwhitney(y1,y2):
    '''
    Check if y1 and y2 stand the assumptions for ttest and if not preform mannwhitney
    :param y1: 1st sample
    :param y2: 2nd sample
    :return: s, pvalue, ttest - True/False
    '''
    ttest = False

    # assumptions for t-test
    # https://pythonfordatascience.org/independent-t-test-python/#t_test-assumptions
    ns1, np1 = stats.shapiro(y1)  # test normality of the data
    ns2, np2 = stats.shapiro(y2)  # test noramlity of the data
    ls, lp = stats.levene(y1, y2)  # test that the variance behave the same
    if (lp > .05) & (np1 > .05) & (np2 > .05):
        ttest = True
        s, p = stats.ttest_ind(y1, y2)
    else:
        s, p = stats.mannwhitneyu(y1, y2)

    return s, p, ttest

def new_dir(dirPath):
    if not os.path.isdir(dirPath):
        os.mkdir(dirPath)

def progress(i, N, text = None):
    '''
    Update progress in the same line
    :param i: current progress
    :param N: total count
    :param text: description text
    :return:
    '''
    sys.stdout.write('/r')
    if text is None:
        sys.stdout.write('Frame {0}/{1} added to video'.format(i, N))
    else:
        sys.stdout.write(text + '{0}/{1}'.format(i, N))
    sys.stdout.flush()