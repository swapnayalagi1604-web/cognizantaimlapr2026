#read linear regression pickle file
import pandas as pd
import pickle
import os

model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'linear_regression_model.pkl')
   
#load the model
with open(model_path, 'rb') as f:
    model = pickle.load(f)
print(f'Model loaded from {model_path}')

#print all the metrics of the model
# Prove it's the same model
print(f"Loaded slope    : {model.coef_[0]:.4f}")
print(f"Loaded intercept: {model.intercept_:.4f}")
print(f"Same object?    : {type(model).__name__}")


#predict the price of a house with 3 bedrooms

Area = 1500
predicted_price = model.predict(pd.DataFrame({'Area': [Area]}))
print(f'Predicted price for a house with {Area} sqft: {predicted_price[0]}')