# feup-ac-22-23

Project of the Machine Learning (AC) curricular unit, development in python.

## How to run

Create virtual environment and install all necessary dependencies:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Execute pipeline and see the results:
```sh
dvc repro
dvc exp show
```

A submission for the kaggle competition can be created by running:
```sh
cd submission
python3 submission.py
```

To execute a statistical comparison test between two models, save the `data/model.joblib` files from any two executions and run:
```sh
python3 src/results_statistic_significance.py path_to_classifier1 path_to_classifier2
```

All the notebooks in the `notebooks` directory assume that the pipeline has been executed at least once.

## Group #41

- Adriano Soares (up201904873@up.pt)
- Filipe Campos (up201905609@up.pt)
- Francisco Cerqueira (up201905337@up.pt)
- Vasco Alves (up201908031@up.pt)