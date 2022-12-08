import sqlite3
import pandas as pd


def main():
    con = sqlite3.connect("data/database.db")

    df = pd.read_sql_query(
        " \
        SELECT account_view.id as accountId, ownerSex, ownerBirthday, ownerCardType, frequency, account_view.date AS accountCreationDate, isShared, balance, loanDev_view.date AS loanDate, duration as loanDuration, payments as loanPayments, amount as loanAmount, ratio, districtName, region, nInhabitants, nMunicipalitiesSub499Inhabitants, nMunicipalities500to1999Inhabitants, nMunicipalities2000to9999Inhabitants, nMunicipalitiesOver10000Inhabitants, nCities, urbanInhabitantsRatio, averageSalary, unemploymentRate95, unemploymentRate96, nEnterpreneursPer1000Inhabitants, commitedCrimes95, commitedCrimes96, \
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
        JOIN district_view ON district_view.id = account_view.districtId;",
        con,
    )

    trans_df = pd.read_sql_query(
        "SELECT * FROM ( \
        select id, accountId, amount as credit, null as withdrawal from transDev where type='credit' \
        UNION \
        select id, accountId, null as credit, amount as withdrawal from transDev where type='withdrawal' or type='withdrawal in cash' \
        );",
        con,
    )

    trans_df["amount"] = (
        trans_df["credit"] if trans_df["withdrawal"].isna else -trans_df["withdrawal"]
    )
    trans_df = (
        trans_df.groupby(["accountId"])
        .apply(lambda x: x.quantile(0.75) - x.quantile(0.25))
        .drop("accountId", axis=1)
    )
    trans_df = df.join(trans_df, on="accountId")
    df["transactionAmountIQR"] = trans_df["amount"]
    df["transactionAmountIQR"] = df["transactionAmountIQR"].fillna(
        df["transactionAmountIQR"].mean()
    )
    df["maxTransactionAmountDistance"] = df["maxTransactionAmountDistance"].fillna(
        df["maxTransactionAmountDistance"].mean()
    )

    df = df.drop("accountId", axis=1)
    df.to_csv("data/unified_data.csv", index=False)


if __name__ == "__main__":
    main()
