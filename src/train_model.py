import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from joblib import dump
import json
import dvc.api

def main():
    # Load train data
    X_train, y_train = pd.read_csv('data/X_train.csv'), pd.read_csv('data/y_train.csv')

    # Load parameters (https://dvc.org/doc/command-reference/params)
    params = dvc.api.params_show()['train']

    # Create model
    model = DecisionTreeClassifier(max_depth=params['max_depth'])
    
    # Train model
    model.fit(X_train, y_train)

    # Store the model to disk (https://scikit-learn.org/stable/model_persistence.html)
    dump(model, 'data/model.joblib')
    
    # Write model parameters to a file
    with open('metrics/model_parameters.json', 'w') as file:
        json.dump(model.get_params(), file)

if __name__ == "__main__":
    main()