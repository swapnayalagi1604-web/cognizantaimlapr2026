#create pca for tshirt data in csv file
#consider target columns QaulityClass, Rest all inputs

import pandas as pd
from sklearn.decomposition import PCA   
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt 
from supervisedmlapp.configurations.conf import T_SHIRT_FILE_PATH
from sklearn.preprocessing import LabelEncoder
import numpy as np
def pca_analysis():
    # Load the dataset
    data = pd.read_csv(T_SHIRT_FILE_PATH)

    #dataset information
    print("Dataset Information:")
    print(data.info())


    #apply label encoding to the target variable
   
    label_encoder = LabelEncoder()
    target_encoder = LabelEncoder()

    y = target_encoder.fit_transform(data['QualityClass'])

    #label encoding to defects, size and stitiching
    data['Defects'] = label_encoder.fit_transform(data['Defects'])
    data['Size'] = label_encoder.fit_transform(data['Size'])
    data['Stitching'] = label_encoder.fit_transform(data['Stitching'])

    #apply one hot encoding to color,fabric,brand
    data = pd.get_dummies(data, columns=['Color', 'Fabric', 'Brand'])   
  
   
    # Separate features and target variable
    X = data.drop('QualityClass', axis=1)  # Features
    
    #print x and y
    print("Features (X):")
    print(X.head())
    print("\nTarget variable (y):")
    print(y[:5])

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # Apply PCA
    pca = PCA(n_components=3)  # Reduce to 2 principal components for visualization
    X_pca = pca.fit_transform(X_scaled) 
    #print principal components
    #computing correlated values
    print("Principal Components:")
    print(X_pca[:5])
    #need how to arrive at the principal components from the original features    
    print("PCA Components column name and values:") 
    
    for i, component in enumerate(pca.components_):
        print(f"Principal Component {i+1}:")
        for feature, value in zip(X.columns, component):
            print(f"  {feature}: {value}") 

    # PC1 importance
    pc1_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': np.abs(pca.components_[0])
    }).sort_values(by='Importance', ascending=False)

    print("Most important features in Principal Component 1:")
    print(pc1_importance.head())


    # PC2 importance
    pc2_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': np.abs(pca.components_[1])
    }).sort_values(by='Importance', ascending=False)
    print("Most important features in Principal Component 2:")
    print(pc2_importance.head())

    # PC3 importance
    pc3_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': np.abs(pca.components_[2])
    }).sort_values(by='Importance', ascending=False)

    

    print("Most important features in Principal Component 3:")
    print(pc3_importance.head())

    #fit the PCA
    pca.fit(X_scaled)
    # Explained variance ratio
    print("Explained Variance Ratio:", pca.explained_variance_ratio_)
    # Features which are reduced by PCA
    print("Features reduced by PCA:", pca.n_components_)

    # Plot PCA
    # Explained variance
    print("\nExplained Variance Ratio:")
    print("PC1:", pca.explained_variance_ratio_[0])
    print("PC2:", pca.explained_variance_ratio_[1])
    print("PC3:", pca.explained_variance_ratio_[2])
    print("Total:", np.sum(pca.explained_variance_ratio_))

    print("\nOriginal feature count:", X.shape[1])
    print("Reduced feature count:", pca.n_components_)

    # Create PCA dataframe for plotting
    pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2","PC3"])
    pca_df["QualityClass"] = target_encoder.inverse_transform(y)

    print("\nPCA DataFrame:")
    print(pca_df.head())

    # PCA scatter plot
    plt.figure(figsize=(10, 6))

    for quality in pca_df["QualityClass"].unique():
        subset = pca_df[pca_df["QualityClass"] == quality]

        plt.scatter(
            subset["PC1"],
            subset["PC2"],
            subset["PC3"],
            label=quality,
            alpha=0.7
        )

    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0] * 100:.2f}% Variance)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1] * 100:.2f}% Variance)")
   # plt.zlabel(f"PC3 ({pca.explained_variance_ratio_[2] * 100:.2f}% Variance)")
    plt.title("PCA Visualization of T-Shirt Quality Classification")
    plt.legend()
    plt.grid(True)
    plt.show()






   


if __name__ == "__main__":
    pca_analysis()