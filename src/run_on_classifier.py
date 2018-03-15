import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict
import operator
# my python files
import src.analytics as tics
import src.plotting_functions as pltfuncs
import src.transforms as trans
import src.hyp_test as hyp
import src.score_model as sc
import src.roc_curve as roc
import src.run_on_classifier as run



# Imports
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
from scipy.stats import kendalltau
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import make_scorer
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, Ridge
from sklearn.pipeline import Pipeline
from basis_expansions.basis_expansions import (
    Polynomial, LinearSpline, NaturalCubicSpline)
from regression_tools.dftransformers import (
    ColumnSelector, Identity, FeatureUnion, MapFeature, Intercept)
from regression_tools.plotting_tools import (
    plot_univariate_smooth,
    bootstrap_train,
    display_coef,
    plot_bootstrap_coefs,
    plot_partial_depenence,
    plot_partial_dependences,
    predicteds_vs_actuals)
from sklearn.metrics import roc_curve, auc

def main():
    pass

def run_classifier(df_, keep, classifier):
    print('\n')
    print('\n')
    print('#--------------------------------------------#')
    print('     Running classifier on {}'.format(keep))
    print('#--------------------------------------------#')
    df = df_.copy()
    df = trans.drop_all_except(df, keep)

    # read in label names csv and send it as dictionary to mapping function
    label_names = ['label', 'attack_category', 'attack_cat_num']
    labels_loc = './data/categories.csv'
    labels_to_categories = pd.read_csv(labels_loc, header=None)
    labels_to_categories.columns = label_names
    col_name = 'label'
    new_col_name = 'attack_category'

    df = trans.rewrite_values(df, dict(zip(labels_to_categories.label, labels_to_categories.attack_cat_num)), col_name, new_col_name)
    df['attack_category'].value_counts()

    # rewrite all except attack_category types 2 to zero, put to new dataframe
    df = trans.rewrite_category2_to_zeros(df)
    # df2['attack_category'].value_counts()
    # df.head()

    # undersample the majority category
    df = trans.split_to_5050(df)
    print('\n')
    print('Modified Y to balance 1s and 0s')
    print(df['attack_category'].value_counts())

    # drop label BEFORE running get dummies on data
    trans.drop_if_in(df, 'label')
    'label' in df

    # dummy-ize
    df = pd.get_dummies(df)

    # Split X and Y
    y = df['attack_category']
    X = df.copy()

    # in order to not throw errors
    if 'attack_category' in X:
        X.drop(['attack_category'], axis=1, inplace=True)
    if 'label' in X:
        X.drop(['label'], axis=1, inplace=True)


   ### REGRESSION
   # Split the dataset into the Training set and Test set
    from sklearn.cross_validation import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Standard Scale the values
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)

    from sklearn.linear_model import LogisticRegression

    # teach classifier the correlations betw X_train and y_train
    classifier.fit(X_train, y_train)

    # Predict the Test set results
    y_pred = classifier.predict(X_test) # vector giving prediction of each of the test set observations
    print('\n')
    TN, FP, FN, TP, accuracy, recall, specificity, false_positive_rate, precision = pltfuncs.my_confusion_matrix(y_test, y_pred)

    return TN, FP, FN, TP, accuracy, recall, specificity, false_positive_rate, precision

if __name__ == "__main__": main()
