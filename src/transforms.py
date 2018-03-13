import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from collections import defaultdict

def main():
    pass

def rewrite_values(df, dict_map, column_name):

    # here we don't want to alter the original dataframe
    df2 = df.copy()

    df2.replace({column_name: dict_map}, inplace=True)

    return df2

def my_create_dummies(df, col_list, column_name):
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
            df3[k] = np.where(df[column_name] == k, 1, 0)

        return df3

if __name__ == "__main__": main()
