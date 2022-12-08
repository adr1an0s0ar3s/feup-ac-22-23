import pandas as pd


def main():
    df = pd.read_csv("data/clean_data0.csv")

    cc95 = pd.to_numeric(df["commitedCrimes95"], errors="coerce")
    diff = df["commitedCrimes96"] - cc95
    average_diff = diff.mean()
    cc95[cc95.isna()] = df["commitedCrimes96"][cc95.isna()] - average_diff
    df["commitedCrimes95"] = cc95.astype(int)

    ur95 = pd.to_numeric(df["unemploymentRate95"], errors="coerce")
    diff = df["unemploymentRate96"] - ur95
    average_diff = diff.mean()
    ur95[ur95.isna()] = df["unemploymentRate96"][ur95.isna()] - average_diff
    df["unemploymentRate95"] = ur95

    df["hasCard"] = df["ownerCardType"].apply(lambda x: not pd.isna(x))
    df = df.drop("ownerCardType", axis=1)

    df.to_csv("data/clean_data1.csv", index=False)


if __name__ == "__main__":
    main()
