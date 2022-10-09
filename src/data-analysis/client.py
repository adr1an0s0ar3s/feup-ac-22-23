import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_number_clients_per_decade_birth(df):
    ax = sns.countplot(df, x=df['birthNumber'].dt.year//10*10)
    ax.bar_label(ax.containers[0])
    plt.xlabel('decade')
    plt.title('Number of clients per decade of birth')
    sns.despine(ax=ax)
    plt.tight_layout()
    plt.savefig('../../analysis_plots/number_clients_per_decade_birth.png')
    plt.clf()

def main():
    con = sqlite3.connect('../../data/database.db')
    df = pd.read_sql_query('SELECT * FROM client;', con, index_col='id')

    df['birthNumber'] = df['birthNumber'].astype('int64')
    df['sex'] = df['birthNumber'].apply(lambda x: 'female' if x / 100 % 100 > 50 else 'male')
    df['birthNumber'] = df['birthNumber'].apply(lambda x: 19000000 + x - 5000 if x / 100 % 100 > 50 else 19000000 + x)
    df['birthNumber'] = pd.to_datetime(df['birthNumber'], format='%Y%m%d')

    plot_number_clients_per_decade_birth(df)

if __name__ == "__main__":
    main()