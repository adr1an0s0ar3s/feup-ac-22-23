import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_issuance_frequency_categories_count(df):
    ax = sns.countplot(df, x="frequency")
    ax.bar_label(ax.containers[0])
    plt.xticks(rotation=10)
    plt.title("Issuance frequency categories count")
    plt.xlabel("frequency of issuance of statements")
    sns.despine(ax=ax)
    plt.savefig(
        "analysis_plots/issuance_frequency_categories_count.png", bbox_inches="tight"
    )
    plt.clf()


def plot_accounts_created_per_year(df):
    ax = sns.countplot(df, x=df["date"].dt.strftime("%Y"))
    ax.bar_label(ax.containers[0])
    plt.title("Number of accounts created per year")
    plt.xlabel("year")
    sns.despine(ax=ax)
    plt.savefig("analysis_plots/accounts_created_per_year.png", bbox_inches="tight")
    plt.clf()


def plot_top_10_districts_with_most_accounts(df, con):
    dist = pd.read_sql_query("SELECT * FROM district;", con, index_col="id")
    top10 = df["districtId"].value_counts().iloc[:10]
    temp = dist.iloc[top10.index - 1][["districtName", "nInhabitants"]]
    temp["count"] = top10

    fig, (ax1, ax2) = plt.subplots(2)

    # Plot 1
    sns.barplot(temp, x="districtName", y="count", ax=ax1)
    ax1.set_xticks([])
    ax1.set_xticklabels([])
    ax1.set_xlabel("")
    ax1.bar_label(ax1.containers[0])
    ax1.set_ylabel("nº of accounts")

    # Plot 2
    sns.barplot(temp, x="districtName", y="nInhabitants", ax=ax2)
    ax2.set_xticklabels(temp["districtName"], rotation="vertical")
    ax2.set_yticks(range(0, 1200001, 200000))
    ax2.set_yticklabels(range(0, 1200001, 200000))
    ax2.set_xlabel("district name")
    ax2.set_ylabel("nº of inhabitants")
    # ax2.bar_label(ax2.containers[0])

    sns.despine(fig=fig)
    fig.suptitle("Top 10 districts with most number of accounts")
    plt.savefig("analysis_plots/top10_districts_most_accounts.png", bbox_inches="tight")
    plt.clf()


def plot_corr_accounts_per_district_with_district_table(df, con):
    dist = pd.read_sql_query("SELECT * FROM district;", con, index_col="id")
    corr = dist.corrwith(df["districtId"].value_counts(), numeric_only=True)
    ax = plt.bar(corr.index, corr.values)
    plt.xticks(rotation=90)
    plt.grid(axis="y")
    plt.title(
        "Correlation between the number of accounts per district and the district table attributes"
    )
    plt.xlabel("district table attributes")
    plt.ylabel("correlation percentage")
    plt.savefig(
        "analysis_plots/corr_accounts_per_district_with_district_table.png",
        bbox_inches="tight",
    )
    plt.clf()


def main():
    con = sqlite3.connect("data/database.db")
    df = pd.read_sql_query("SELECT * FROM account;", con, index_col="id")
    df["date"] = pd.to_datetime(df["date"], format="%y%m%d")
    plot_issuance_frequency_categories_count(df)
    plot_accounts_created_per_year(df)
    plot_top_10_districts_with_most_accounts(df, con)
    plot_corr_accounts_per_district_with_district_table(df, con)


if __name__ == "__main__":
    main()
