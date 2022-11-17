from sklearn.model_selection import train_test_split
import pandas as pd

def main():
    df = pd.read_csv('data/prepared_data.csv')

    # Obtain independent and target variables
    X, y = df.drop('status', axis=1), df['status']

    max_test_size=0.40
    test_size = 0.1
    while test_size <= max_test_size:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, shuffle=False, stratify=None)
        print(f"test_size={test_size:01f}: train={y_train.mean():02f} - test={y_test.mean():02f} -> diff={y_train.mean()-y_test.mean():02f} | (Target: {y.mean()})")
        test_size += 0.01

    # Split into test and train data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, shuffle=False, stratify=None)
    
    # Save split data
    X_train.to_csv('data/X_train_not_sampled.csv', index=False)
    y_train.to_csv('data/y_train_not_sampled.csv', index=False)
    X_test.to_csv('data/X_test_all_features.csv', index=False)
    y_test.to_csv('data/y_test.csv', index=False)

if __name__ == '__main__':
    main()