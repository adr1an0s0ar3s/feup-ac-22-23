import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE 

def sample(X, y):
    smote = SMOTE(random_state=42)
    X, y = smote.fit_resample(X, y)
    return X, y

def sort(X, y):
    index = np.argsort(X['loanDate'])
    return X.iloc[index], y.iloc[index]

def main():
    # Read processed data
    df = pd.read_csv('data/prepared_data.csv')

    # Obtain independent and target variables
    X, y = df.drop('status', axis=1), df['status']

    X, y = sample(X, y)
    X, y = sort(X, y)
    X.to_csv('data/X.csv', index=False)
    y.to_csv('data/y.csv', index=False)

if  __name__ == '__main__':
    main()