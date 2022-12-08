import pandas as pd
import numpy as np
from sklearn.linear_model import (
    Perceptron,
    LogisticRegression,
    SGDClassifier,
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import (
    VarianceThreshold,
    SelectKBest,
    SelectPercentile,
    RFECV,
    SequentialFeatureSelector,
    chi2,
    f_regression,
)
import dvc.api

estimators = {
    "perceptron": Perceptron(),
    "dt": DecisionTreeClassifier(),
    "lr": LogisticRegression(),
    "sgd": SGDClassifier(),
}
dvc_params = dvc.api.params_show()
fs_params = dvc_params["feature_selection"]
base_estimator = estimators[fs_params["estimator"]]

filters = {
    "variance": VarianceThreshold(threshold=0.5),
    "kbest": SelectKBest(),
    "kbest-chi2": SelectKBest(score_func=chi2),
    "kbest-f_regression": SelectKBest(score_func=f_regression),
    "percentile": SelectPercentile(percentile=25),
}

wrappers = {
    "rfecv": RFECV(
        estimator=base_estimator,
        step=1,
        cv=StratifiedKFold(2),
        scoring="accuracy",
        min_features_to_select=1,
    ),
    "forward": SequentialFeatureSelector(
        estimator=base_estimator, n_features_to_select="auto", direction="forward"
    ),
    "backward": SequentialFeatureSelector(
        estimator=base_estimator, n_features_to_select="auto", direction="backward"
    ),
}


def select(X_train, y_train, X_test, selector):
    selector.fit(X_train, np.ravel(y_train))
    print(X_train.columns[[x for x in selector.get_support()]])
    X_train = pd.DataFrame(
        selector.transform(X_train), columns=X_train.columns[selector.get_support()]
    )
    X_test = pd.DataFrame(
        selector.transform(X_test), columns=X_test.columns[selector.get_support()]
    )
    return X_train, X_test


def automatic_feature_selection(X_train, X_test):
    y_train = pd.read_csv("data/y_train.csv")

    if fs_params["filter"] != "none":
        X_train, X_test = select(X_train, y_train, X_test, filters[fs_params["filter"]])

    if fs_params["wrapper"] != "none":
        X_train, X_test = select(
            X_train, y_train, X_test, wrappers[fs_params["wrapper"]]
        )

    return X_train, X_test


def manual_feature_selection(X_train, X_test):
    selected_features = dvc_params["manual_feature_selection_fields"]

    return X_train[selected_features], X_test[selected_features]


def main():
    X_train = pd.read_csv("data/X_train_all_features.csv")
    X_test = pd.read_csv("data/X_test_all_features.csv")

    if dvc_params["manual_feature_selection"]:
        X_train, X_test = manual_feature_selection(X_train, X_test)
    else:
        X_train, X_test = automatic_feature_selection(X_train, X_test)

    with open("data/features.csv", "w") as file:
        file.write(",".join(list(X_train.columns)))

    X_train.to_csv("data/X_train.csv", index=False)
    X_test.to_csv("data/X_test.csv", index=False)


if __name__ == "__main__":
    main()
