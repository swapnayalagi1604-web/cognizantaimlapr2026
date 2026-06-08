#create linear regression model for house price prediction
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
    X = data[['Area']] # Features
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

    #pack the model using pickle
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'linear_regression_model.pkl')
    # Create the models/ folder if it doesn't already exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f'Model saved to {model_path}')

    #create onnx model
    # ---------- ONNX EXPORT ----------
    # Step 1: describe the input — 1 feature (Area in sqft), any batch size
    initial_type = [("float_input", FloatTensorType([None, 1]))]

    # Step 2: convert the already-trained model
    onnx_model = convert_sklearn(model, initial_types=initial_type)

    # Step 3: save the ONNX model to a file
    onnx_model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'linear_regression_model.onnx')
    os.makedirs(os.path.dirname(onnx_model_path), exist_ok=True)

    #Step 4: write the ONNX model to disk 
    with open(onnx_model_path, "wb") as f:
        f.write(onnx_model.SerializeToString())

    print(f'ONNX model saved to {onnx_model_path}')

    #plot the regression line
    plt.scatter(X_test, y_test, color='blue', label='Actual')
    plt.plot(X_test, y_pred, color='red', label='Predicted')
    plt.xlabel('Bedrooms')
    plt.ylabel('Price')
    plt.title('Linear Regression: Bedrooms vs Price')
    plt.legend()
    plt.show()
    
    return model

if __name__ == "__main__":
    linear_regression_model()