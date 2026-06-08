#create light gbm for churn prediction csv data
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from supervisedmlapp.configurations.conf import CHURN_FILE_PATH
from sklearn.metrics import confusion_matrix
def train_light_gbm(data_path):
    # Load the dataset
    data = pd.read_csv(data_path)

   

    # Encode string columns to integers so LightGBM can accept them
    string_cols = data.select_dtypes(include=['object', 'string']).columns
    for col in string_cols:
        data[col] = LabelEncoder().fit_transform(data[col].astype(str))

    # Assuming the target variable is named 'PlanDowngradeHistory' and the rest are features
    X = data.drop('PlanDowngradeHistory', axis=1)
    y = data['PlanDowngradeHistory']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create the LightGBM dataset
    lgb_train = lgb.Dataset(X_train, label=y_train)
    lgb_eval = lgb.Dataset(X_test, label=y_test, reference=lgb_train)

    # num_leaves and min_data_in_leaf are kept small to match the dataset size (100 rows)
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'boosting_type': 'gbdt',
        'num_leaves': 8,
        'min_data_in_leaf': 5,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'verbose': -1
    }

    # Train the model
    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=100,
                    valid_sets=lgb_eval,
                    callbacks=[lgb.early_stopping(10, verbose=False)]
                   )

    # Predict on the test set
    y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    y_pred_binary = [1 if pred > 0.5 else 0 for pred in y_pred]

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred_binary)
    print(f'Accuracy: {accuracy:.4f}')
    #print classification report
    print(classification_report(y_test, y_pred_binary))
    

    cm = confusion_matrix(y_test, y_pred_binary)
    #confusion matrix
    print("Confusion Matrix:")
    print(cm)

if __name__ == "__main__":
    data_path = CHURN_FILE_PATH  # Update with your actual data path
    train_light_gbm(data_path)