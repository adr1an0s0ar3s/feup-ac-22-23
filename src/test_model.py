import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, average_precision_score, roc_auc_score, precision_recall_curve
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
    print(y_pred_prob)
    print('\n\n\n')
    print(y_pred)

    # Calculate metrics
    #live = Live('evaluation')
    #live.log_plot("roc", y_test.values.tolist(), y_pred.tolist())
    #live.log("avg_prec", average_precision_score(y_test, y_pred))
    #live.log("roc_auc", roc_auc_score(y_test, y_pred))

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Write metric results to disk
    with open("metrics/results.json", 'w') as file:
        json.dump({
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }, file)

if __name__ == "__main__":
    main()