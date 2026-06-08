#create random forest tree for crop disease dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import data
from supervisedmlapp.configurations.conf import CROP_FILE_PATH

def random_forest_tree():
    # Load the dataset
    data = pd.read_csv(CROP_FILE_PATH)

    #encode leaf color, spot pattern,season and disease
    data['LeafColor'] = data['LeafColor'].astype('category').cat.codes
    data['SpotPattern'] = data['SpotPattern'].astype('category').cat.codes
    data['Season'] = data['Season'].astype('category').cat.codes
   
    

    # Assuming the last column is the target variable and the rest are features
    X = data.iloc[:, :-1]  # Features
    y = data.iloc[:, -1]   # Target variable

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=0.2,
                                                          random_state=42,
                                                          stratify=y)

    # Create a Random Forest Classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)

    # Fit the model to the training data
    rf_classifier.fit(X_train, y_train)

    # Predict on the test set
    y_pred = rf_classifier.predict(X_test)

    # Evaluate the model
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    disease_cat = data['PlanDowngradeHistory'].astype('category')
    disease_mapping = dict(enumerate(disease_cat.cat.categories))
    data['Disease'] = disease_cat.cat.codes
    print("Disease Name and Encoded Value:")
    for code, disease in disease_mapping.items():
        print(f"{disease}: {code}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

if __name__ == "__main__":
    random_forest_tree()