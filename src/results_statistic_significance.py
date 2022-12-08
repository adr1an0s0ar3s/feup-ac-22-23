# Using a 5 x 2 CV test as described in (https://ieeexplore.ieee.org/document/6790639)
# Based on the following implementation https://www.kaggle.com/code/ogrellier/parameter-tuning-5-x-2-fold-cv-statistical-test/notebook

import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from joblib import load

parser = argparse.ArgumentParser()
parser.add_argument("classifier1_path")
parser.add_argument("classifier2_path")

def get_score_from_model(model, val_x, val_y):
    preds = model.predict_proba(val_x)[:, 1]
    return roc_auc_score(val_y, preds)

def main():
    args = parser.parse_args()
    classifier1 = load(args.classifier1_path)
    classifier2 = load(args.classifier2_path)

    df = pd.read_csv("data/prepared_data.csv")
    X, y = df.drop("status", axis=1), df["status"]
    
    # Choose seeds for each 2-fold iterations
    seeds = [13, 51, 137, 24659, 347]

    # Initialize the score difference for the 1st fold of the 1st iteration 
    p_1_1 = 0.0
    # Initialize a place holder for the variance estimate
    s_sqr = 0.0
    # Initialize scores list for both classifiers
    scores_1 = []
    scores_2 = []

    # Iterate through 5 2-fold CV
    for i_s, seed in enumerate(seeds):
        # Split the dataset in 2 parts with the current seed
        folds = StratifiedKFold(n_splits=2, shuffle=True, random_state=seed)
        # Initialize score differences
        p_i = np.zeros(2)
            
        # Go through the current 2 fold
        for i_f, (train_idx, val_idx) in enumerate(folds.split(X, y)):
            train_x, train_y = X.iloc[train_idx], y.iloc[train_idx]
            val_x, val_y = X.iloc[val_idx], y.iloc[val_idx]

            # Reset the classifiers
            classifier1.random_state = seed
            classifier2.random_state = seed

            # Fit the data
            classifier1.fit(train_x, train_y)
            classifier2.fit(train_x, train_y)
            
            # keep score history for mean and stdev calculation
            scores_1.append(get_score_from_model(classifier1, val_x, val_y))
            scores_2.append(get_score_from_model(classifier2, val_x, val_y))

            # Compute score difference for current fold  
            p_i[i_f] = scores_1[-1] - scores_2[-1]

            # Keep the score difference of the 1st iteration and 1st fold
            if (i_s == 0) & (i_f == 0):
                p_1_1 = p_i[i_f]

        # Compute mean of scores difference for the current 2-fold CV
        p_i_bar = (p_i[0] + p_i[1]) / 2

        # Compute the variance estimate for the current 2-fold CV
        s_i_sqr = (p_i[0] - p_i_bar) ** 2 + (p_i[1] - p_i_bar) ** 2 

        # Add up to the overall variance
        s_sqr += s_i_sqr
    
    # Compute t value as the first difference divided by the square root of variance estimate
    t_bar = p_1_1 / ((s_sqr / 5) ** .5) 

    diff_scores = list(i-j for i,j in zip(scores_1, scores_2))

    print(f"Classifier 1: mean score = {np.mean(scores_1)} | stdev = {np.std(scores_1)}")
    print(f"Classifier 2: mean score = {np.mean(scores_2)} | stdev = {np.std(scores_2)}")
    print(f"Score difference mean + stdev : {np.mean(diff_scores)}, {np.std(diff_scores)}")
    print(f"t_value for the current test is {t_bar}")

if __name__ == "__main__":
    main()