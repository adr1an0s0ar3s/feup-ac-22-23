import sqlite3
import pandas as pd

def main():
    con = sqlite3.connect('data/database.db')
    df = pd.read_sql_query('SELECT * FROM loanDev', con)
    df = df.drop('id', axis=1)
    df.to_csv('data/processed_data.csv', index=False)

if  __name__ == '__main__':
    main()