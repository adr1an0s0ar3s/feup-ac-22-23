import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def convert_to_unix_timestamp(df, attribute):
    df[attribute] = df[attribute].apply(lambda x: "19" + str(x))
    df[attribute] = pd.to_datetime(df[attribute], format="%Y%m%d").map(pd.Timestamp.timestamp)
    return df

def main():
    df = pd.read_csv('data/clean_data.csv')

    for attribute in ['ownerBirthday', 'accountCreationDate', 'loanDate']:
        df = convert_to_unix_timestamp(df, attribute)
    
    df = pd.get_dummies(df, columns=['frequency', 'region'], drop_first=True)
    
    df["districtName"] = LabelEncoder().fit_transform(df["districtName"])

    # Roughly scale dataset
    scaler = StandardScaler().fit(df)
    scaled_df = pd.DataFrame(data=scaler.transform(df), columns=df.columns)
    scaled_df['status'] = df['status']

    scaled_df.to_csv('data/prepared_data.csv', index=False)

if  __name__ == '__main__':
    main()