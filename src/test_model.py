import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, average_precision_score, roc_auc_score, precision_recall_curve, roc_auc_score
from dvclive import Live
import math
import os
import json

def main():
    # Load model from disk
    model = load('data/model.joblib')
    
    # Load test data
    X_test, y_test = pd.read_csv('data/X_test.csv'), pd.read_csv('data/y_test.csv')

    # Predict test data
    y_pred = model.predict(X_test)
    y_pred_prob = model.predict_proba(X_test)
    
    # Calculate metrics
    live = Live('evaluation')
    live.log_plot("roc", y_test.values.astype(int), y_pred_prob[:, 1])

    # ... but actually it can be done with dumping data points into a file:
    # ROC has a drop_intermediate arg that reduces the number of points.
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html#sklearn.metrics.roc_curve.
    # PRC lacks this arg, so we manually reduce to 1000 points as a rough estimate.
    precision, recall, prc_thresholds = precision_recall_curve(y_test, y_pred_prob[:, 1])
    nth_point = math.ceil(len(prc_thresholds) / 1000)
    prc_points = list(zip(precision, recall, prc_thresholds))[::nth_point]
    prc_file = os.path.join("evaluation", "plots", "precision_recall.json")
    with open(prc_file, "w") as fd:
        json.dump(
            {
                "prc": [
                    {"precision": p, "recall": r, "threshold": t}
                    for p, r, t in prc_points
                ]
            },
            fd,
            indent=4,
        )

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred)

    # Write metric results to disk
    with open("metrics/results.json", 'w') as file:
        json.dump({
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'auc': roc_auc
        }, file)

if __name__ == "__main__":
    main()