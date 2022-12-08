import pandas as pd
from imblearn.over_sampling import SMOTE


def sample(X, y):
    smote = SMOTE(random_state=42)
    X, y = smote.fit_resample(X, y)
    return X, y


def main():
    # Read processed data
    X = pd.read_csv("data/X_train_not_sampled.csv")
    y = pd.read_csv("data/y_train_not_sampled.csv")

    X, y = sample(X, y)
    X.to_csv("data/X_train_all_features.csv", index=False)
    y.to_csv("data/y_train.csv", index=False)


if __name__ == "__main__":
    main()
