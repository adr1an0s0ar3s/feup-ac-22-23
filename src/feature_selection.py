import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold, SelectKBest

def select(X, y, selector):
    selected_X = selector.fit_transform(X, np.ravel(y))
    print(X.columns[[x for x in selector.get_support()]])
    X = pd.DataFrame(selected_X, columns=X.columns[selector.get_support()])
    return X, y

def main():
    X = pd.read_csv('data/sampled_X.csv')
    y = pd.read_csv('data/sampled_y.csv')

    # X, y = select(X, y, VarianceThreshold(threshold=.1))
    X, y = select(X, y, SelectKBest(k=10))

    X.to_csv('data/X.csv', index=False)
    y.to_csv('data/y.csv', index=False)

if __name__ == '__main__':
    main()