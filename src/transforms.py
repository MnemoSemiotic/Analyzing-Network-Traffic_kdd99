import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from collections import defaultdict

def main():
    pass

def rewrite_values(df, dict_map, col_name, new_col_name):
    '''
    INPUT:  a pandas dataframe
           dict of column values to with values that should map to them
           string with the new column name
    Return: Return a new dataframe with new column added, all values
           represented by their categories
    '''
    # here we don't want to alter the original dataframe
    df2 = df.copy()

    df2[new_col_name] = 0


    df2[new_col_name] = df.apply(lambda row: dict_map[row[col_name]], axis=1)

    return df2

# def _rewrite_helper(df, dict_map, col_name):
#     if df[col_name] == dict_map[]

def my_create_dummies(df, col_list, col_name):
        '''
        INPUT:  a pandas dataframe
               list of column values to be dummy-ized
               string with the column name to extract dummy values from
        Return: Return the dataframe with new columns added, all values
               set to zero except those that correspond to the correct
               mapping
        '''
        df3 = df.copy()
        for k in col_list:
            df3[k] = 0

        for k in col_list:
            df3[k] = np.where(df[col_name] == k, 1, 0)

        return df3

if __name__ == "__main__": main()
