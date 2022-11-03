import pandas as pd

def main():
    df = pd.read_csv('data/clean_data0.csv')

    cc95 = pd.to_numeric(df['commitedCrimes95'], errors='coerce')
    cc95[cc95.isna()] = df[cc95.isna()]['commitedCrimes96']
    df['commitedCrimes95'] = cc95.astype(int)

    df['unemploymentRate96'] = df['unemploymentRate96'].astype(int)
    ur95 = pd.to_numeric(df['unemploymentRate95'], errors='coerce')
    ur95[ur95.isna()] = df[ur95.isna()]['unemploymentRate96']
    df['unemploymentRate95'] = ur95.astype(int)

    df['hasCard'] = df['ownerCardType'].apply(lambda x: False if pd.isna(x) else True)
    df = df.drop('ownerCardType', axis=1)

    df.to_csv('data/clean_data1.csv', index=False)

if __name__ == "__main__":
    main()