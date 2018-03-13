import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from collections import defaultdict

def main():
    pass

def rewrite_values(df, dict_map, column_name):
    '''
    INPUT: a pandas dataframe
           dict mapping column values to new value
           string with the column name to search/change values in
    Return: Return a copy of the dataframe with the values changed
    '''
    # here we don't want to alter the original dataframe
    df2 = df.copy()

    df2.replace({column_name: dict_map}, inplace=True)

    return df2

if __name__ == "__main__": main()
