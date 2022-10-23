import pandas as pd

def main():
    df = pd.read_csv('data/clean_data0.csv')
    df.to_csv('data/clean_data1.csv')

if __name__ == "__main__":
    main()