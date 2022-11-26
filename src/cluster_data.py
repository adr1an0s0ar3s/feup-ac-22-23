import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

def main():
    df = pd.read_csv("data/prepared_data.csv")
    X, y = df[['balance', 'timesIntoNegativeBalance','numTransactionsNegBalance']], df['status']
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit_predict(X)
    print(kmeans.cluster_centers_)
    print(f"KMeans Silhouette score: {silhouette_score(X, kmeans.labels_)}")
    dbscan = DBSCAN(eps=1.6, min_samples=5)
    dbscan.fit_predict(X)
    print(f"DBSCAN Silhouette score: {silhouette_score(X, dbscan.labels_)}")

if __name__ == "__main__":
    main()