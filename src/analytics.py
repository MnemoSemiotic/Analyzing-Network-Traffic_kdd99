import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict

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

def count_column_zeros(df):
    '''
        INPUT: a pandas dataframe
        Return: dictionary of the zero ratio in each
                column of a dataframe
                {'column_name': 0.57...
                }
    '''
    return {col:df[col][df[col] == 0].count() / len(df)
            for col in df.select_dtypes(include=['object', 'int64]').columns}

if __name__ == "__main__": main()
