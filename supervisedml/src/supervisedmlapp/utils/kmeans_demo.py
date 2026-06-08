#create k-means demo for customer segmentation using customers.csv file
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from supervisedmlapp.configurations.conf import CUSTOMER_FILE_PATH
# Load the dataset
data = pd.read_csv(CUSTOMER_FILE_PATH)
# Select relevant features for clustering
features = data[['Age', 'AnnualIncome_k']]
# Determine the optimal number of clusters using the elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(features)
    wcss.append(kmeans.inertia_)
# Plot the elbow method graph
plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Elbow Method for Optimal Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()
# Automatically detect the elbow: point with maximum perpendicular distance
# from the line connecting the first and last WCSS values
x = np.arange(1, 11, dtype=float)
y = np.array(wcss)
x_norm = (x - x.min()) / (x.max() - x.min())
y_norm = (y - y.min()) / (y.max() - y.min())
dx, dy = x_norm[-1] - x_norm[0], y_norm[-1] - y_norm[0]
distances = np.abs(dy * x_norm - dx * y_norm + x_norm[-1] * y_norm[0] - y_norm[-1] * x_norm[0]) / np.sqrt(dx**2 + dy**2)
optimal_clusters = int(x[np.argmax(distances)])
print("Optimal number of clusters based on the elbow method:", optimal_clusters)
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', random_state=42)
data['Cluster'] = kmeans.fit_predict(features)
# Visualize the clusters
plt.figure(figsize=(10, 5))
plt.scatter(data['Age'], data['AnnualIncome_k'], c=data['Cluster'], cmap='viridis')
plt.title('Customer Segmentation using K-Means')
plt.xlabel('Age')
plt.ylabel('Annual Income (k$)')
plt.show()

