import pandas as pd
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt
import datetime

def plot_amount_boxplot(df):
    fig, ax = plt.subplots(1,2)

    sns.boxplot(df['amount'], ax=ax[0])
    ax[0].set_title("Loan Amount")
    ax[0].set_xticklabels([])
    ax[0].set_xticks([])
    ax[0].set_ylabel('Amount (Kč)')

    sns.boxplot(df['payments'], ax=ax[1])
    ax[1].set_title("Monthly Payment")
    ax[1].set_xticklabels([])
    ax[1].set_xticks([])

    fig.tight_layout()
    plt.savefig('analysis_plots/loan_amount_boxplot.png')

def plot_amount_over_time(df):
    sns.lmplot(data=df, x='timestamp', y='amount')
    plt.ylabel('Amount (Kč)')
    plt.xlabel('Year')
    plt.title('Distribution of loan amount over time')

    years = [datetime.datetime(1993+i, 1, 1, 0, 0).timestamp() for i in range(0,5)]
    plt.xticks(ticks=years,labels=[93, 94, 95, 96, 97])
    plt.tight_layout()
    plt.savefig('analysis_plots/loan_amount_over_time.png')

def plot_amount_distribution(df):
    tmp_df = df.copy()
    tmp_df['status'] = df['status'].apply(lambda x: 'Yes' if x == 1 else 'No')

    plot = sns.displot(tmp_df, x='amount', hue='status', kde=True, palette=['#E1812C', '#8E9A9D'])
    plot._legend.remove()
    plt.title('Loan amount distribution')
    plt.xlabel('Amount (Kč)')
    plt.legend(['Yes', 'No'], title='Loan paid')
    plt.savefig('analysis_plots/loan_amount_distribution0.png')

    plot = sns.displot(tmp_df, x='amount', hue='status', stat='density', col='status', common_norm=False, kde=True, palette=['#E1812C', '#8E9A9D'], col_order=['Yes', 'No'])
    plot.axes[0,0].set_xlabel('Amount (Kč)')
    plot.axes[0,1].set_xlabel('Amount (Kč)')
    plt.tight_layout()
    
    plt.savefig('analysis_plots/loan_amount_distribution1.png')


def date_to_timestamp(date):
    Y = int("19" + date[:2])
    M = int(date[2:4])
    D = int(date[4:])
    return datetime.datetime(Y,M,D, 0, 0).timestamp()

def main():
    con = sqlite3.connect('data/database.db')
    df = pd.read_sql_query('SELECT * FROM loanDev', con)
    df['timestamp'] = df['date'].apply(date_to_timestamp)
    plot_amount_boxplot(df)
    plot_amount_over_time(df)
    plot_amount_distribution(df)


if __name__ == '__main__':
    main()