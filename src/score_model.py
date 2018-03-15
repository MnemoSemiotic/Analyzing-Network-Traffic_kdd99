import numpy as np

def rmsle(actual, predictions):
    # log_diff = np.log(predictions+1) - np.log(actual+1)
    # return np.sqrt(np.mean(log_diff**2))
    mse = ((actual - predictions)**2).mean()
    return np.sqrt(mse)

if __name__=='__main__':
    actual = np.array([10000, 10000, 50000, 50000, 100000, 100000])
    predictions = np.array([5000, 15000, 45000, 55000, 95000, 105000])
    error = rmsle(actual, predictions)
    print(error)
