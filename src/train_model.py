import json
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from joblib import dump
import dvc.api


available_clfs = {
    "dt": (
        DecisionTreeClassifier(),
        {
            "criterion": ["gini", "entropy", "log_loss"],
            "splitter": ["best", "random"],
            "max_depth": [5, 10, 15, None],
            "min_samples_split": [2, 3, 4],
            "min_samples_leaf": [1, 2, 3],
            "min_weight_fraction_leaf": [0.0],
            "max_features": ["sqrt", "log2", None],
            "max_leaf_nodes": [None],
        },
    ),
    "knn": (
        KNeighborsClassifier(),
        {
            "n_neighbors": [1, 3, 5, 10],
            "weights": ["uniform", "distance"],
            "algorithm": ["ball_tree", "kd_tree", "brute"],
            "leaf_size": [20, 30, 40],
            "p": [1, 2],
            "metric": ["minkowski"],
        },
    ),
    "rf": (
        RandomForestClassifier(),
        {
            "n_estimators": [5, 10, 25, 50, 100],
            "criterion": ["gini", "entropy", "log_loss"],
            "max_leaf_nodes": [None],
        },
    ),
    "svm": (
        SVC(),
        {
            "C": [1],
            "kernel": [
                "linear",
                "poly",
                "rbf",
                "sigmoid",
            ],  # 'precomputed' needs a square kernel matrix so it's not tested
            "degree": [2, 3, 4],
            "gamma": ["scale", "auto"],
            "probability": [True],
        },
    ),
    "nb": (GaussianNB(), {}),
    "ada": (
        AdaBoostClassifier(),
        {"n_estimators": [5, 10, 25, 50, 100], "learning_rate": [0.5, 1.0, 1.5]},
    ),
}


def main():
    # Load train data
    X_train, y_train = pd.read_csv("data/X_train.csv"), pd.read_csv("data/y_train.csv")

    # Load parameters (https://dvc.org/doc/command-reference/params)
    input_clfs = dvc.api.params_show()["classifiers"]
    params = dvc.api.params_show()["params"]
    execute_grid_search = params == {}

    if execute_grid_search:

        best_models = []
        scores = []

        for input_clf in input_clfs:
            # Obtain classifier and param_grid
            clf, param_grid = available_clfs.get(input_clf, None)
            if clf is None:
                continue

            # Exhaustive search over specified parameter values
            # for an estimator to find the best one
            best_model = GridSearchCV(
                clf,
                param_grid,
                scoring="roc_auc",
                n_jobs=-1,
                refit=True,
                cv=StratifiedKFold(n_splits=5, shuffle=False),
                verbose=1,
            )

            start_time = time.time()

            # Train model
            best_model.fit(X_train, np.ravel(y_train))

            fit_time = time.time() - start_time

            best_models.append((input_clf, best_model.best_params_))
            scores.append(best_model.best_score_)

        best_clf_name, params = best_models[scores.index(max(scores))]
        model = available_clfs[best_clf_name][0]
        model.set_params(**params)
        start_time = time.time()
        model.fit(X_train, np.ravel(y_train))
        fit_time = time.time() - start_time

    else:

        # Obtain classifier
        model = available_clfs[input_clfs[0]][0]

        # Set parameters
        model.set_params(**params)

        # Train model
        start_time = time.time()
        model.fit(X_train, np.ravel(y_train))
        fit_time = time.time() - start_time

    # Store the model to disk (https://scikit-learn.org/stable/model_persistence.html)
    dump(model, "data/model.joblib")

    # Write model parameters to a file
    with open("metrics/model_details.json", "w") as file:
        json.dump(
            {
                "model": model.__class__.__name__,
                "params": model.get_params(),
                "fit_time": fit_time,
            },
            file,
        )


if __name__ == "__main__":
    main()
