#create cnn model classification using tf and keras for Rosary Church.jpeg image and save the model in resources folder
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from deepmlapp.configurations.conf import MODEL_FILE_PATH
import matplotlib.pyplot as plt

plt.rc('image', cmap='gray')
plt.rc('figure', autolayout=True)


image_path = MODEL_FILE_PATH

#use opencv to read the image and convert it to grayscale

image = tf.io.read_file(image_path)
image = tf.io.decode_jpeg(image, channels=1)  
image = tf.image.resize(image, [300, 300])
image = tf.image.convert_image_dtype(image, tf.float32)

print("Original Image Shape:", image.shape)
'''
plot the original image to visualize it before applying any transformations. This helps us understand the input data and the effects of subsequent operations.
'''
plt.figure(figsize=(5,5))
plt.imshow(tf.squeeze(image))
plt.savefig('original_image.png')
plt.title("Original Image")
plt.axis('off')
plt.show()

# Add batch dimension
image = tf.expand_dims(image, axis=0)
'''
Define Convolution Kernel
We define an edge detection filter (Laplacian kernel) to extract important image features.
'''


kernel = tf.constant([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
], dtype=tf.float32)

kernel = tf.reshape(kernel, [3, 3, 1, 1])

conv_output = tf.nn.conv2d(
    input=image,
    filters=kernel,
    strides=[1, 1, 1, 1],
    padding='SAME'
)
'''
Apply Convolution Layer
The convolution layer applies the filter to the image to detect edges and features.
'''
print("After Convolution Shape:", conv_output.shape)

plt.figure(figsize=(5,5))
plt.imshow(tf.squeeze(conv_output))
plt.title("After Convolution")
plt.axis('off')
plt.savefig('after_convolution.png')
plt.show()
'''
Apply ReLU Activation
'''
relu_output = tf.nn.relu(conv_output)

print("After ReLU Shape:", relu_output.shape)

plt.figure(figsize=(5,5))
plt.imshow(tf.squeeze(relu_output))
plt.title("After ReLU Activation")
plt.axis('off')
plt.savefig('after_relu.png')
plt.show()

pool_output = tf.nn.max_pool2d(
    input=relu_output,
    ksize=[1, 2, 2, 1],
    strides=[1, 2, 2, 1],
    padding='SAME'
)
# Apply Max Pooling to reduce spatial dimensions and retain important features.
print("After Pooling Shape:", pool_output.shape)

plt.figure(figsize=(5,5))
plt.imshow(tf.squeeze(pool_output))
plt.title("After Max Pooling")
plt.axis('off')
plt.savefig('after_max_pooling.png')
plt.show()

#apply Flattening to convert the 2D feature maps into a 1D vector for further processing in fully connected layers.
flatten_layer = tf.keras.layers.Flatten()
flatten_output = flatten_layer(pool_output)

print("After Flatten Shape:", flatten_output.shape)

print("First 20 Flattened Values:")
print(flatten_output.numpy()[0][:20])

#add fully connected layer to learn complex patterns from the extracted features.
dense_layer = tf.keras.layers.Dense(
    units=64,         
    activation='relu' 
)

dense_output = dense_layer(flatten_output)

print("After Fully Connected Layer Shape:", dense_output.shape)
