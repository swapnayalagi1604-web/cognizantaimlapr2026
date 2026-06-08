#create multi linear regression model for house price prediction
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression   
from sklearn.metrics import mean_squared_error, r2_score
from supervisedmlapp.configurations.conf import HOUSE_FILE_PATH
import matplotlib.pyplot as plt
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import pickle
def linear_regression_model():
    # Load the dataset
    data = pd.read_csv(HOUSE_FILE_PATH)
    
    # Define features and target variable
    X = data.drop('Price', axis=1) # Features
    y = data['Price']  # Target variable
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Create a linear regression model
    model = LinearRegression()
    
    # Fit the model to the training data
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)**0.5
    r2 = r2_score(y_test, y_pred)
    
    print(f'Mean Squared Error: {mse}')
    print(f'R^2 Score: {r2}')

    #print the coefficients of the model
    print(f'Coefficients: {model.coef_}')
    #print the intercept of the model
    print(f'Intercept: {model.intercept_}')
    #new x values for prediction
    new_X = pd.DataFrame({'Area': [1500], 'Bedrooms': [3], 'Bathrooms': [2],'Parking': [1],'Property_Age': [10],'School_Distance': [8]})
    predicted_price = model.predict(new_X)
    print(f'Predicted Price for new data: {predicted_price[0]}')

    
    # For multiple regression, plot actual vs predicted values
    plt.scatter(y_test, y_pred, color='blue', label='Predictions', alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--', label='Perfect Fit')
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.title('Multiple Linear Regression: Actual vs Predicted Price')
    plt.legend()
    plt.show()
    
    return model

if __name__ == "__main__":
    linear_regression_model()