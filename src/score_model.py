import numpy as np

def main():
    pass

def rmsle(actual, predictions):
    # log_diff = np.log(predictions+1) - np.log(actual+1)
    # return np.sqrt(np.mean(log_diff**2))
    mse = ((actual - predictions)**2).mean()
    return np.sqrt(mse)

if __name__=='__main__':main()
