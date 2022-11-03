import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE 

def sample(X, y):
    smote = SMOTE(random_state=42)
    X, y = smote.fit_resample(X, y)
    return X, y

def sort(X, y):
    index = np.argsort(X['loanDate'])
    return X.iloc[index], y.iloc[index]

def split(X, y):
    # Split into test and train data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, shuffle=False, stratify=None)
    
    # Save split data
    X_train.to_csv('data/X_train.csv', index=False)
    X_test.to_csv('data/X_test.csv', index=False)
    y_train.to_csv('data/y_train.csv', index=False)
    y_test.to_csv('data/y_test.csv', index=False)

def main():
    # Read processed data
    df = pd.read_csv('data/prepared_data.csv')

    # Obtain independent and target variables
    X, y = df.drop('status', axis=1), df['status']

    X, y = sample(X, y)
    X, y = sort(X, y)

    split(X, y)

if  __name__ == '__main__':
    main()