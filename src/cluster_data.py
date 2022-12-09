import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, MeanShift
from sklearn.metrics import (
    silhouette_score,
    v_measure_score,
    completeness_score,
    homogeneity_score,
)
import json


def dbscan(X, y):
    best_model = None
    max_score = 0

    for eps in np.linspace(0.1, 5, 20):
        for min_samples in range(1, 11):
            for algorithm in ["auto", "ball_tree", "kd_tree", "brute"]:
                for p in [1, 2, 3]:
                    dbscan = DBSCAN(
                        eps=eps, min_samples=min_samples, algorithm=algorithm, p=p
                    )
                    y_pred = dbscan.fit_predict(X)
                    score = v_measure_score(y, y_pred)
                    if score > max_score:
                        best_model = dbscan
                        max_score = score

    y_pred = best_model.fit_predict(X)
    return {
        "silhouette": silhouette_score(X, best_model.labels_),
        "v_measure": v_measure_score(y, y_pred),
        "completeness_score": completeness_score(y, y_pred),
        "homogeneity": homogeneity_score(y, y_pred),
    }


def kmeans(X, y):
    best_model = None
    max_score = 0

    # Grid Search
    for init in ["k-means++", "random"]:
        for max_iter in [50, 150, 300, 500]:
            for algorithm in ["lloyd", "elkan"]:
                kmeans = KMeans(
                    n_clusters=2, init=init, max_iter=max_iter, algorithm=algorithm
                )
                y_pred = kmeans.fit_predict(X)
                score = v_measure_score(y, y_pred)
                if score > max_score:
                    best_model = kmeans
                    max_score = score

    y_pred = best_model.fit_predict(X)
    return {
        "silhouette": silhouette_score(X, best_model.labels_),
        "v_measure": v_measure_score(y, y_pred),
        "completeness_score": completeness_score(y, y_pred),
        "homogeneity": homogeneity_score(y, y_pred),
    }


def mean_shift(X, y):

    meanshift = MeanShift()
    y_pred = meanshift.fit_predict(X)
    return {
        "silhouette": silhouette_score(X, meanshift.labels_),
        "v_measure": v_measure_score(y, y_pred),
        "completeness_score": completeness_score(y, y_pred),
        "homogeneity": homogeneity_score(y, y_pred),
    }


def main():
    df = pd.read_csv("data/prepared_data.csv")
    X, y = (
        df[["balance", "timesIntoNegativeBalance", "numTransactionsNegBalance"]],
        df["status"],
    )

    results = dbscan(X, y)
    # Write metric results to disk
    with open("metrics/dbscan_results.json", "w") as file:
        json.dump(results, file)

    results = kmeans(X, y)
    with open("metrics/kmeans_results.json", "w") as file:
        json.dump(results, file)

    results = mean_shift(X, y)
    with open("metrics/meanshift_results.json", "w") as file:
        json.dump(results, file)


if __name__ == "__main__":
    main()
