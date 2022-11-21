import pandas as pd
import sqlite3
from sklearn.preprocessing import LabelEncoder, StandardScaler
from joblib import load

def convert_to_unix_timestamp(df, attribute):
    df[attribute] = df[attribute].apply(lambda x: "19" + str(x))
    df[attribute] = pd.to_datetime(df[attribute], format="%Y%m%d").map(pd.Timestamp.timestamp)
    return df

def main():
    con = sqlite3.connect('data/database.db')

    df = pd.read_sql_query(' \
        SELECT loanDev_view.id as loanId, account_view.id as accountId, ownerSex, ownerBirthday, ownerCardType, frequency, account_view.date AS accountCreationDate, isShared, balance, loanDev_view.date AS loanDate, duration as loanDuration, payments as loanPayments, amount as loanAmount, ratio, districtName, region, nInhabitants, nMunicipalitiesSub499Inhabitants, nMunicipalities500to1999Inhabitants, nMunicipalities2000to9999Inhabitants, nMunicipalitiesOver10000Inhabitants, nCities, urbanInhabitantsRatio, averageSalary, unemploymentRate95, unemploymentRate96, nEnterpreneursPer1000Inhabitants, commitedCrimes95, commitedCrimes96, \
        medianAmount, \
        sumAllTransactions, \
        insurancePaymentsCount, \
        insurancePaymentsAverage, \
        timesIntoNegativeBalance, \
        numTransactions, \
        numTransactionsNegBalance, \
        numExternalBankTransactions, \
        withdrawalCount, \
        cashWithdrawalCount,  \
        withdrawalAnyMethodCount,  \
        creditCount \
        maxWithdrawal, \
        maxCredit, \
        maxTransactionAmountDistance, \
        sumSanctionInterest, \
        avgSanctionInterest,  \
        hasStableIncome,    \
        status \
        FROM loanDev_view \
        JOIN account_view ON account_view.id = loanDev_view.accountId \
        JOIN owners_sex_birthday_view ON owners_sex_birthday_view.accountId = account_view.id \
        LEFT OUTER JOIN owners_card_type ON owners_card_type.accountId = account_view.id \
        JOIN district_view ON district_view.id = account_view.districtId;'
    , con)

    trans_df = pd.read_sql_query("SELECT * FROM ( \
        select id, accountId, amount as credit, null as withdrawal from transDev where type='credit' \
        UNION \
        select id, accountId, null as credit, amount as withdrawal from transDev where type='withdrawal' or type='withdrawal in cash' \
        );"
    , con)

    trans_df['amount'] = trans_df['credit'] if trans_df['withdrawal'].isna else -trans_df['withdrawal']

    trans_df = trans_df.groupby(['accountId']).apply(lambda x: x.quantile(0.75) - x.quantile(0.25)).drop('accountId', axis=1)
    trans_df = df.join(trans_df, on='accountId')
    df['transactionAmountIQR'] = trans_df['amount']
    df['transactionAmountIQR'] =df['transactionAmountIQR'].fillna(df['transactionAmountIQR'].mean())
    df['maxTransactionAmountDistance'] = df['maxTransactionAmountDistance'].fillna(df['maxTransactionAmountDistance'].mean())

    df = df.drop('accountId', axis=1)

    cc95 = pd.to_numeric(df['commitedCrimes95'], errors='coerce')
    diff = df['commitedCrimes96'] - cc95
    averageDiff = diff.mean()
    cc95[cc95.isna()] = df['commitedCrimes96'][cc95.isna()] - averageDiff
    df['commitedCrimes95'] = cc95.astype(int)

    ur95 = pd.to_numeric(df['unemploymentRate95'], errors='coerce')
    diff = df['unemploymentRate96'] - ur95
    averageDiff = diff.mean()
    ur95[ur95.isna()] = df['unemploymentRate96'][ur95.isna()] - averageDiff
    df['unemploymentRate95'] = ur95

    df['hasCard'] = df['ownerCardType'].apply(lambda x: False if pd.isna(x) else True)
    df = df.drop('ownerCardType', axis=1)

    for attribute in ['ownerBirthday', 'accountCreationDate', 'loanDate']:
        df = convert_to_unix_timestamp(df, attribute)

    df = pd.get_dummies(df, columns=['frequency', 'region'], drop_first=True)

    df["districtName"] = LabelEncoder().fit_transform(df["districtName"])

    # Roughly scale dataset
    scaler = load('../data/scaler.joblib')
    scaled_df = df.drop('loanId', axis=1)
    scaled_df = pd.DataFrame(data=scaler.transform(scaled_df), columns=scaled_df.columns)
    scaled_df['status'] = df['status']
    scaled_df['loanId'] = df['loanId']

    scaled_df.to_csv('data/prepared_data.csv', index=False)
    df = scaled_df

    features = []
    with open('../data/features.csv') as file:
        features = file.readline().split(',')

    ids, df = df['loanId'], df[features]

    print(df.head())

    model = load('../data/model.joblib')

    binary_predictions = model.predict(df)
    print(binary_predictions)
    predictions = model.predict_proba(df)
    print(predictions[:,1])
    print(f"Ratio:{sum(binary_predictions)/len(binary_predictions)}")

    with open("submission.csv", "w") as file:
        file.write('Id,Predicted\n')
        for i, pred in zip(ids, predictions[:,1]):
            file.write(f"{i},{pred}\n")

if __name__ == "__main__":
    main()