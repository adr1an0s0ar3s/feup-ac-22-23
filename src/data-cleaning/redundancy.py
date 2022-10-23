import pandas as pd

def main():
    df = pd.read_csv('data/unified_data.csv')
    df.to_csv('data/clean_data0.csv')

if __name__ == "__main__":
    main()