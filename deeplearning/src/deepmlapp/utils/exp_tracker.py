import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import mlflow
import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import numpy as np
import tf2onnx

from deepmlapp.configurations.conf import LOAN_FILE_PATH


file_path = LOAN_FILE_PATH

data = pd.read_csv(file_path)
print("Dataset loaded successfully!")

data['LoanStatus'] = data['LoanStatus'].map({
    'Rejected': 0,
    'Approved': 1
})

x = data.drop(['LoanStatus', 'ApplicantID'], axis=1)
y = data['LoanStatus']

x_raw = x.values.astype(np.float32)
y_raw = y.values.astype(np.float32)


with mlflow.start_run():

    mlflow.log_param("model_type", "pipeline_nn_with_normalization")
    mlflow.log_param("epochs", 10)
    mlflow.log_param("batch_size", 32)

    normalizer = layers.Normalization(
        axis=-1,
        name="standard_scaler_layer"
    )

    normalizer.adapt(x_raw)

    pipeline_input = tf.keras.Input(
        shape=(3,),
        name="loan_raw_input"
    )

    pipeline_x = normalizer(pipeline_input)
    pipeline_x = layers.Dense(64, activation='relu')(pipeline_x)
    pipeline_x = layers.Dense(32, activation='relu')(pipeline_x)

    pipeline_output = layers.Dense(
        1,
        activation='sigmoid',
        name="loan_output"
    )(pipeline_x)

    pipeline_model = tf.keras.Model(
        inputs=pipeline_input,
        outputs=pipeline_output,
        name="loan_pipeline_model"
    )

    pipeline_model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    pipeline_model.fit(
        x_raw,
        y_raw,
        epochs=10,
        batch_size=32
    )

    pipeline_loss, pipeline_accuracy = pipeline_model.evaluate(
        x_raw,
        y_raw
    )

    print("Pipeline Loss:", pipeline_loss)
    print("Pipeline Accuracy:", pipeline_accuracy)

    mlflow.log_metric("pipeline_loss", pipeline_loss)
    mlflow.log_metric("pipeline_accuracy", pipeline_accuracy)

    pipeline_model.save("loan_approval_pipeline.keras")
    mlflow.log_artifact("loan_approval_pipeline.keras")

    mlflow.tensorflow.log_model(
        pipeline_model,
        artifact_path="loan_pipeline_model",
        registered_model_name="LoanApprovalPipelineModel"
    )

    input_signature = [
        tf.TensorSpec(
            shape=[None, 3],
            dtype=tf.float32,
            name="loan_raw_input"
        )
    ]

    onnx_model, _ = tf2onnx.convert.from_keras(
        pipeline_model,
        input_signature=input_signature,
        opset=13
    )

    with open("loan_approval_pipeline.onnx", "wb") as f:
        f.write(onnx_model.SerializeToString())

    mlflow.log_artifact("loan_approval_pipeline.onnx")

    print("Pipeline model converted to ONNX successfully!")
    print("Run ID:", mlflow.active_run().info.run_id)
    print("Model registered successfully")

print("Experiment logged successfully!")