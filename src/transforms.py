import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from collections import defaultdict
import src.analytics as tics

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

# split to 50% 0s, 50% 1s
def split_to_5050(df):
    val_counts = df['attack_category'].value_counts()
    if val_counts[0] < val_counts[1]:
        N = val_counts[0]
        # print('removed {} rows'.format(val_counts[1]-val_counts[0]))
    else:
        N = val_counts[1]
        # print('removed {} rows'.format(val_counts[0]-val_counts[1]))
    return df.sample(frac=1).groupby('attack_category', sort=False).head(N)

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
            # print('dropped {}'.format(i))

def drop_if_in(df, col_name):
    if col_name in df:
        df.drop(col_name, axis=1, inplace=True)
        # print('dropped {}'.format(col_name))

def drop_high_correlations(df_, pos_thresh=0.6, neg_thresh=-0.6):
    # gets a dictionary of the top encoded features
    top_correlations = tics.get_top_correlations(df_, .6, -.6)

    # Time to actually drop some features, in particular anything correlated above .80 above
    for column in top_correlations:
        drop_if_in(df_, column[0])

    return df_

def drop_all_except(df_, keep):
    for i in list(df_.columns):
        if i != 'label' and i not in keep and i !='attack_category':
            drop_if_in(df_, i)
    return df_

if __name__ == "__main__": main()
