import pandas as pd

def main():
    df = pd.read_csv('data/clean_data_1.csv')
    df.to_csv('data/clean_data.csv')

if __name__ == "__main__":
    main()