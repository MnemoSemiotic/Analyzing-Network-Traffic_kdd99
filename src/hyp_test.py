import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict

def main():
    pass

def get_attacks_proportion(df, match):
    df2 = df[(df.protocol_type == match)]
    print('Number of {} Connections: {}'.format(match,len(df2)))
    attacks = len(df2[(df2.attack_category != 0)])
    print('Number of Attacks: {}'.format(attacks))
    normal = len(df2[(df2.attack_category == 0)])
    print('Number Normal: {}'.format(normal))

    print('Cat   Count')
    print(df2['attack_category'].value_counts())

    return attacks, normal

if __name__ == "__main__": main()
