import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold, SelectKBest

def select(X_train, y_train, X_test, selector):
    selector.fit(X_train, np.ravel(y_train))
    print(X_train.columns[[x for x in selector.get_support()]])
    X_train = pd.DataFrame(selector.transform(X_train), columns=X_train.columns[selector.get_support()])
    X_test = pd.DataFrame(selector.transform(X_test), columns=X_test.columns[selector.get_support()])
    return X_train, X_test

def main():
    X_test = pd.read_csv('data/X_test_all_features.csv')
    X_train = pd.read_csv('data/X_train_all_features.csv')
    y_train = pd.read_csv('data/y_train.csv')

    # X, y = select(X, y, VarianceThreshold(threshold=.1))
    X_train, X_test = select(X_train, y_train, X_test, SelectKBest(k=10))

    X_train.to_csv('data/X_train.csv', index=False)
    X_test.to_csv('data/X_test.csv', index=False)

if __name__ == '__main__':
    main()