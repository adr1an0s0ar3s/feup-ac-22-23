import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, average_precision_score, roc_auc_score, precision_recall_curve, roc_auc_score
from dvclive import Live
import math
import os
import json
import time

def main():
    # Load model from disk (https://scikit-learn.org/stable/model_persistence.html)
    model = load('data/model.joblib')
    
    # Load test data
    X_test, y_test = pd.read_csv('data/X_test.csv'), pd.read_csv('data/y_test.csv')

    # Predict test data
    # Useful read: predict() vs predict_proba() - https://towardsdatascience.com/predict-vs-predict-proba-scikit-learn-bdc45daa5972
    y_pred = model.predict(X_test)

    start_time = time.time()

    y_pred_prob = model.predict_proba(X_test)

    predict_time = time.time() - start_time
    
    # Calculate metrics (https://dvc.org/doc/dvclive/api-reference/live)
    live = Live('evaluation')
    live.log_plot("roc", y_test.values.astype(int), y_pred_prob[:, 1], drop_intermediate=False)

    precision, recall, prc_thresholds = precision_recall_curve(y_test, y_pred_prob[:, 1])
    prc_points = list(zip(precision, recall, prc_thresholds))
    prc_file = os.path.join("evaluation", "plots", "precision_recall.json")
    with open(prc_file, "w") as file:
        json.dump({
            "prc": [
                {"precision": p, "recall": r, "threshold": t}
                for p, r, t in prc_points
            ]
        }, file, indent=4)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_prob[:,1])

    # Write metric results to disk
    with open("metrics/results.json", 'w') as file:
        json.dump({
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'auc': roc_auc,
            'predict_time': predict_time,
        }, file)

if __name__ == "__main__":
    main()