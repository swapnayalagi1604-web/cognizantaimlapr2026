#use tf and keras for loan processing and modeling 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd

from deepmlapp.configurations.conf import LOAN_FILE_PATH


def simple_nn_process():
    data=pd.read_csv(LOAN_FILE_PATH)
    data=data.dropna()
    # Convert categorical variables to numerical using one-hot encoding
    #label encoding for loan_status
    data['LoanStatus'] = data['LoanStatus'].map({'Rejected': 0, 'Approved': 1})
    #identify x and y
    x=data.drop(['LoanStatus','ApplicantID'],axis=1)
    y=data['LoanStatus']
    #apply standard scalar
    scaler=StandardScaler()
    x_scaled=scaler.fit_transform(x)
    y_scaled=y.values
    #build a simple nn model tensor flow with keras
    model=tf.keras.Sequential([
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(x_scaled, y_scaled, epochs=10, batch_size=32)
    #evaluate the model
    loss, accuracy = model.evaluate(x_scaled, y_scaled)
    print(f"Loss: {loss}, Accuracy: {accuracy}")
    #print the model summary
    print(model.summary())
    #print metrics
    print(f"Metrics: {model.metrics_names}")
    #confusion matrix
    print("Confusion Matrix:")
    y_pred = (model.predict(x_scaled) > 0.5).astype("int32")
   
    print(confusion_matrix(y_scaled, y_pred))
    #print the model weights
    #print("Model Weights:")
    '''
    for layer in model.layers:
        weights = layer.get_weights()
        print(weights)
    '''
   #precision, recall, f1-score
   
    print("Classification Report:")
    print(classification_report(y_scaled, y_pred))



if __name__ == "__main__":
    simple_nn_process()



