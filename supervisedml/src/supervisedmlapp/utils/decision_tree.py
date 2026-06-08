#create decision tree model for loan.csv for loan approval prediction
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from supervisedmlapp.configurations.conf import LOAN_FILE_PATH  
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
def create_decision_tree_model():
    # Load the dataset
    data = pd.read_csv(LOAN_FILE_PATH)
    
    # Preprocess the data (handle missing values, encode categorical variables, etc.)
    data = data.dropna()  # Drop rows with missing values for simplicity

    # Define features and target variable before one-hot encoding
    y = (data['LoanApproved'] == 'Yes').astype(int)
    X = pd.get_dummies(data.drop('LoanApproved', axis=1))  # One-hot encode features only
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and fit the Decision Tree model
    model = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)
    
    print(f'Accuracy: {accuracy}')
    print('Classification Report:')
    print(report)
    print('Confusion Matrix:')
    print(confusion)
    #draw the decision tree with all the features and class names
    
    plt.figure(figsize=(10,10))
    plot_tree(model, feature_names=X.columns, class_names=['Approved', 'Not Approved'], filled=True)
    plt.show()

if __name__ == "__main__":
    create_decision_tree_model()