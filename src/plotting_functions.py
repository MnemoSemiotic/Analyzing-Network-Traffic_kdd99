import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    pass

def plot_hist_basic(df, col):
    """Return a Matplotlib axis object with a histogram of the data in col.

    Plots a histogram from the column col of dataframe df.

    Parameters
    ----------
    df: Pandas DataFrame

    col: str
        Column from df with numeric data to be plotted

    Returns
    -------
    ax: Matplotlib axis object
    """

    data = df[col]
    ax = data.hist(bins=20, normed=1, edgecolor='none', figsize=(14, 7), alpha=.5)
    ax.set_ylabel('Probability Density')
    ax.set_title(col)
    plt.xticks(rotation=40)
    return ax

def corr_heat(df, title):
    # corr = df.corr()
    # mask = np.zeros_like(corr, dtype=np.bool)
    # mask[np.triu_indices_from(mask)] = True
    # f, ax = plt.subplots(figsize=(12, 12))
    # cmap = sns.diverging_palette(220, 10, as_cmap=True)
    # sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
    #             square=True, linewidths=.5, cbar_kws={"shrink": .5},xticklabels=corr.index, yticklabels=corr.columns)
    # plt.xticks(rotation=60, ha="right")
    # plt.yticks(rotation=0)
    # ax.set_title("Correlation Heat Map")
    # plt.show()
    corr = df.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(17,15))
    cmap = sns.color_palette('coolwarm')
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True, linewidths=.5,
                yticklabels=True, annot=True, fmt='.2f', cbar_kws={'shrink':.5})
    plt.title(title, fontsize=20)
    plt.xticks(rotation=90, fontsize=11)
    plt.yticks(rotation=0, fontsize=11)
    plt.tight_layout()


def covariance(x,y):
    '''
        INPUT: a numpy array or pandas scalar
        Return: the covariance of the data
    '''
    cov = 0
    x_mean = x.mean()
    y_mean = y.mean()
    '''
    for ind in range(len(x.index)):
        cov += (x[ind]-x_mean)*(y[ind]-y_mean)
        '''
    cov = ((x-x_mean)*(y-y_mean)).sum()
    return cov/len(x.index)


def correlation(x,y):
    '''
        INPUT: a numpy array or pandas scalar
        Return: the correlation of the data
    '''
    return covariance(x,y)/(x.std()*y.std())

def log_label_for_factor_plot(df, col_name, x, hue, title):
    '''
        INPUT:        df: pandas dataframe
                col_name: column name for the x-axis
                       x: what item in column to filter by
                     hue: column name for y axis(what is being plotted against)
        Return: NONE, displays factorplot
    '''
    df2 = df[(df.protocol_type == x)]

    g = sns.factorplot(x=col_name,
                       hue=hue,
                       data=df2,
                       kind='count',
                       size=8,
                       aspect=.9)

    for ax, title in zip(g.axes.flat, title):
        ax.set_title(title)
        ax.set(yscale="log")

def my_confusion_matrix(y_test, y_pred, col):
    # Making Confusion Matrix
    from sklearn.metrics import confusion_matrix


    conf_mat = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = confusion_matrix(y_test, y_pred).ravel()

    if TP + TN + FP + FN > 0:
        accuracy = (TP + TN)/(TP + TN + FP + FN)
    else:
        accuracy = 0

    if TP + TN + FP + FN > 0:
        classification_error  = (FP + FN)/(TP + TN + FP + FN)
    else:
        classification_error = 0

    # Sensitivity/True Positive Rate/Recall: When the actual value is positive, how often is the prediction correct?
    if TP + FN > 0:
        recall = TP / (TP + FN)
    else:
        recall = 0 # ignore d/b0

    # Specificity: When the actual value is negative, how often is the prediciton correct?
    if TN + FP > 0:
        specificity = TN / (TN + FP)
    else:
        specificity = 0 # ignore d/b0

    # False Positive Rate: When the actual value is negative, how often is the prediction incorrect?
    if TN + FP > 0:
        false_positive_rate = FP / (TN + FP)
    else:
        false_positive_rate = 0 # ignore d/b0

    # False negative rate (FNR)
    if FN + TP > 0:
        false_negative_rate = FN / (FN + TP)
    else:
        false_negative_rate = 0

    # Precision: When a positive value is predicted, how often is the prediction incorrect?false_positive_rate = FP / (TN + FP)
    if TP + FP > 0:
        precision = TP / (TP + FP)
    else:
        precision = 0 # ignore d/b0



    print('True Positives: {}'.format(TP))
    print('True Negatives: {}'.format(TN))
    print('False Positives: {}'.format(FP))
    print('True Negatives: {}'.format(FN))
    print()
    print('Accuracy: {}'.format(accuracy))
    print('Classification_error: {}'.format(classification_error))
    print('Recall: {}'.format(recall))
    print('Precision: {}'.format(precision))
    print('False Negative Rate: {}'.format(false_negative_rate))
    print()
    print('confusion matrix')
    print(conf_mat)

    plot_confusion_matrix(conf_mat, title='{}_Confusion_Matrix'.format(str(col[0])))

    return TN, FP, FN, TP, accuracy, recall, specificity, false_positive_rate, false_negative_rate, precision

def plot_confusion_matrix(cm, title='Confusion_Matrix', cmap=plt.cm.Blues):

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar
    plt.tight_layout
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    filename = 'images/{}.png'.format(title)
    # plt.savefig(filename)


if __name__ == "__main__": main()
