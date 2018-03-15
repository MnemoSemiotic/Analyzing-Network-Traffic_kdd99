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

if __name__ == "__main__": main()
