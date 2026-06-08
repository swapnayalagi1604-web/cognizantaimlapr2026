#create polynomial regression model for the population dataset

import pandas as pd
import matplotlib.pyplot as plt

from supervisedmlapp.configurations.conf import POPULATION_FILE_PATH
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def polynomial_regression_model():
    data = pd.read_csv(POPULATION_FILE_PATH)

    X = data[['Year']]
    y = data['Population']

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42
    )

    polynomial_features = PolynomialFeatures(degree=4)

    X_train_poly = polynomial_features.fit_transform(X_train)
    X_test_poly = polynomial_features.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_poly, y_train)

    y_pred = model.predict(X_test_poly)

    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

    print(f'RMSE: {rmse}')
    print(f'R^2 Score: {r2}')

    year_2020 = pd.DataFrame({'Year': [2020]})
    year_2020_poly = polynomial_features.transform(year_2020)

    population_2020 = model.predict(year_2020_poly)

    actual_population_2020 = data[data['Year'] == 2020]['Population'].values[0]

    difference = actual_population_2020 - population_2020[0]

    print(f'Actual population for the year 2020: {actual_population_2020}')
    print(f'Predicted population for the year 2020: {population_2020[0]}')
    print(f'Difference between actual and predicted population for the year 2020: {difference}')

    X_range = pd.DataFrame({
        'Year': range(
            X['Year'].min(),
            X['Year'].max() + 1
        )
    })

    X_range_poly = polynomial_features.transform(X_range)
    y_range_pred = model.predict(X_range_poly)

    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Actual Population')
    plt.plot(
        X_range['Year'],
        y_range_pred,
        color='red',
        linewidth=3,
        label='Polynomial Regression Curve'
    )

    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title('Polynomial Regression - Population Growth')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    polynomial_regression_model()