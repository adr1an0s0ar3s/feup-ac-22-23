import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

def plot_corr_matrix(df):
    fig, ax1 = plt.subplots(figsize=(18,8))
    corr = df.drop(['id', 'accountId'], axis=1).corr(numeric_only=True)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    ax1.set_title("Correlation Matrix")
    sns.heatmap(corr, cmap=sns.diverging_palette(230, 20, as_cmap=True), vmax=1, vmin=-1, annot=True, mask=mask, ax=ax1)
    plt.tight_layout()
    plt.savefig('analysis_plots/district_corr.png')

def plot_loan_by_region(df):
    region_df = df.copy()
    region_df['status'] = (region_df['status']+1)/2 # Transform status from -1/1 to 0/1 to improve plot
    region_df = region_df.groupby('region') \
                            .agg(count=('region', 'count'), mean_status=('status', 'mean'), median_status=('status', 'median')) \
                            .reset_index()
    region_df = region_df.sort_values(by=['count'], ascending=False).reset_index(drop=True)
    region_df['mean_status_percent'] = region_df['mean_status']*100

    fig, ax = plt.subplots(1,2)
    sns.barplot(data=region_df.sort_values(by='region'), x='region', y='mean_status_percent', ax=ax[0])
    ax[0].set_xlabel('Region')
    ax[0].set_ylabel('Loans paid successfully (%)')
    ax[0].set_title('Loans by Region')
    ax[0].xaxis.set_tick_params(rotation=90)

    sns.countplot(data=df.sort_values(by='region'), x='region', hue='status', ax=ax[1])
    ax[1].set_xlabel('Region')
    ax[1].set_ylabel('Count')
    ax[1].set_title('Loans by Region')
    ax[1].xaxis.set_tick_params(rotation=90)
    ax[1].legend(['No', 'Yes'], title='Paid')

    plt.tight_layout()
    plt.savefig('analysis_plots/district_loan_by_region.png')

def plot_loan_by_district(df):
    district_df = df.copy()
    district_df['status'] = (district_df['status']+1)/2 # Transform status from -1/1 to 0/1 to improve plot
    district_df = district_df.groupby('districtName') \
                            .agg(count=('districtName', 'count'), mean_status=('status', 'mean'), median_status=('status', 'median')) \
                            .reset_index()
    district_df = district_df.sort_values(by=['count'], ascending=False).reset_index(drop=True)
    district_df['mean_status_percent'] = district_df['mean_status']*100

    ax1 = sns.set_style(style=None, rc=None )
    fig, ax1 = plt.subplots(figsize=(12,6))

    sns.lineplot(data=district_df['count'], marker='o', sort = False, ax=ax1, color='b')
    ax2 = ax1.twinx()

    plot = sns.barplot(y='mean_status', x='districtName', data=district_df, alpha=0.5, ax=ax2)
    plt.setp(ax1.get_xticklabels(), rotation=90)

    plt.plot([-1,73],[0.719512, 0.719512], color='r')

    red_patch = mpatches.Patch(color='red', label='Average loan payment percentage')
    blue_patch = mpatches.Patch(color='blue', label='Sample Count')
    plt.legend(handles=[red_patch, blue_patch])

    ax1.set_ylabel('Count', color='b')
    ax2.set_ylabel('Loans paid successfully (%)')

    plt.title('Loan payment rate per district')

    plt.tight_layout()
    plt.savefig('analysis_plots/district_loan_by_district.png')

def main():
    con = sqlite3.connect('data/database.db')
    df = pd.read_sql_query('SELECT * FROM loanDev JOIN (select account.id, district.id as districtId, districtName, region, nInhabitants, nMunicipalitiesSub499Inhabitants, nMunicipalities500to1999Inhabitants, nMunicipalities2000to9999Inhabitants, nMunicipalitiesOver10000Inhabitants, nCities, urbanInhabitantsRatio, averageSalary, unemploymentRate95, unemploymentRate96, nEnterpreneursPer1000Inhabitants, commitedCrimes95, commitedCrimes96 from account JOIN district where account.districtId = district.id) as A where loanDev.accountId = A.id;', con)
    plot_corr_matrix(df)
    plot_loan_by_region(df)
    plot_loan_by_district(df)

if __name__ == '__main__':
    main()