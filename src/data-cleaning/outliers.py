import pandas as pd


def main():
    df = pd.read_csv("data/clean_data1.csv")
    df.to_csv("data/clean_data.csv", index=False)


if __name__ == "__main__":
    main()
