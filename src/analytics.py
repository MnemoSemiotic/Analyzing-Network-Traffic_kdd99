import os

def main():
    pass

def create_random_samples(filepath, n_samples=1000, filename='subsample_0.csv'):
    '''
    using coreutils gshuf, create a random sample
    '''
    os.system('gshuf -n {} {} > {}'.format(n_samples, filepath, filename))

if __name__ == "__main__": main()
