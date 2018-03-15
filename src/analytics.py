import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict
import operator

def main():
    pass

def create_random_samples(filepath, n_samples=1000, outputname='subsample_0.csv'):
    '''
    using coreutils gshuf, create a random sample
    requires brew install coreutils

    if using on linux, change gshuf to shuf
    '''
    os.system('gshuf -n {} {} > {}'.format(n_samples, filepath, outputname))

def count_column_uniques(df):
    '''
        INPUT: a pandas dataframe
        Return: dictionary of the unique values in each
                column of a dataframe
                {'column_name': ['unique_val_1', 'unique_val_2']...
                }
    '''
    return {col:list(df[col].unique())
            for col in df.select_dtypes(include=['object']).columns}

def count_zeros_ratio(df):
    '''
        INPUT: a pandas dataframe
        Return: dictionary of the zero ratio and count in each
                column of a dataframe
                {'column_name': [percent, count] ...
                }
    '''

    return {col: [df[col][df[col] == 0].count() / len(df), df[col][df[col] == 0].count()]
            for col in df.select_dtypes(include=['object', 'int64']).columns}

def count_zeros_message(df):
    '''
    INPUT: a pandas dataframe
    Return: String with message giving column names that have only
            zeros for the sample counted
    '''
    zero_counts = count_zeros_ratio(df)
    message = 'At {} samples:\n'.format(len(df))
    for k, v in zero_counts.items():
        if v[1] == len(df):
            message += ('   {} has only zero values\n'.format(k))
    return message

def count_categories(df):
    '''
    INPUT: a pandas dataframe
    Return: dictionary with keys of column names and
            values of the count of unique items in
            each column
    '''
    subset = df.select_dtypes(include=['object'])
    cat_dict = {}
    for column in df.columns:
        cat_dict[column] = df.groupby(column).count().shape[0]
    return cat_dict

def get_top_correlations(df, pos_thresh, neg_thresh):
    '''
    INPUT: df: a pandas dataframe
           pos_thresh: value to filter above (ie .6 for greater than .6)
           neg_thresh: value to filter below
    Return: dictionary with keys of column names and
            highly correlated column name
    '''
    c = df.corr()

    s = c.unstack()
    so = s.sort_values(kind="quicksort", ascending=False).dropna()

    so = so[so < 1]
    so = so[so > pos_thresh]
    so = so[so > -1]
    so = so[so > pos_thresh]
    so = so[::2]
    return dict(so)

if __name__ == "__main__": main()
