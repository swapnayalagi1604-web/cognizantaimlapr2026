#create logistic regression model for bank loan dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from supervisedmlapp.configurations.conf import BANK_FILE_PATH
import matplotlib.pyplot as plt
import seaborn as sns
# Load the dataset
def logistic_regression_model():
    data = pd.read_csv(BANK_FILE_PATH)
    
    # Assuming the target variable is 'loan_status' and the rest are features
    X = data.drop('loan_status', axis=1)
    y = data['loan_status']
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and fit the logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    #plot the graph of confusion matrix
   
    plt.figure(figsize=(10,7))
    #blue and light blue color for the heatmap
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

    
    return accuracy, report, conf_matrix

if __name__ == "__main__":
    accuracy, report, conf_matrix = logistic_regression_model()
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(conf_matrix)