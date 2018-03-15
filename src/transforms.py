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

def rewrite_category2_to_zeros(df):
    df['attack_category'].replace([1,3,4], 0, inplace=True)
    df['attack_category'].replace(2, 1, inplace=True)
    return df

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

def read_data(sample_name):
    # Create list of column names
    columns = ['duration',
           'protocol_type',
           'service',
           'flag',
           'src_bytes',
           'dst_bytes',
           'land',
           'wrong_fragment',
           'urgent',
           'hot',
           'num_failed_logins',
           'logged_in',
           'num_compromised',
           'root_shell',
           'su_attempted',
           'num_root',
           'num_file_creations',
           'num_shells',
           'num_access_files',
           'num_outbound_cmds',
           'is_host_login',
           'is_guest_login',
           'count',
           'srv_count',
           'serror_rate',
           'srv_serror_rate',
           'rerror_rate',
           'srv_rerror_rate',
           'same_srv_rate',
           'diff_srv_rate',
           'srv_diff_host_rate',
           'dst_host_count',
           'dst_host_srv_count',
           'dst_host_same_srv_rate',
           'dst_host_diff_srv_rate',
           'dst_host_same_src_port_rate',
           'dst_host_srv_diff_host_rate',
           'dst_host_serror_rate',
           'dst_host_srv_serror_rate',
           'dst_host_rerror_rate',
           'dst_host_srv_rerror_rate',
           'label']
    df = pd.read_csv(sample_name, header=None)
    df.columns = columns
    return df

# Drop columns with zero values
def drop_zeros_columns(df):
    for i in list(df.columns):
        if df[i].min() == df[i].max():
            df.drop([i], axis=1, inplace=True)
            print('dropped {}'.format(i))

if __name__ == "__main__": main()
