import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#load the MNIST dataset - 10 digits (0-9) handwritten images
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

#normalize the pixel values to be between 0 and 1
x_train, x_test = x_train / 255.0, x_test / 255.0

#build a simple model with a callback to stop training when accuracy reaches 99%
model = keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    #neurons in the hidden layer dropped out randomly during training to prevent overfitting
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

#define callbacks for early stopping and model checkpointing
early_stopping = keras.callbacks.EarlyStopping(monitor='accuracy', patience=3, mode='max', restore_best_weights=True)
model_checkpoint = keras.callbacks.ModelCheckpoint('best_model.h5', monitor='accuracy', save_best_only=True, mode='max')

#add callbacks to the training process
model.fit(x_train, y_train, epochs=20, 
          callbacks=[early_stopping, model_checkpoint],
          batch_size=64,
          validation_split=0.2
          
          )
#evaluate the model on the test set
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print('\nTest accuracy:', test_acc)


