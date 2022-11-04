from sklearn.model_selection import train_test_split
import pandas as pd

def main():
    X, y = pd.read_csv('data/X.csv'), pd.read_csv('data/y.csv')
    # Split into test and train data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, shuffle=False, stratify=None)
    
    # Save split data
    X_train.to_csv('data/X_train.csv', index=False)
    X_test.to_csv('data/X_test.csv', index=False)
    y_train.to_csv('data/y_train.csv', index=False)
    y_test.to_csv('data/y_test.csv', index=False)

if __name__ == '__main__':
    main()