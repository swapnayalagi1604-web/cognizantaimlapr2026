#rabbitmq connection
import pika

from configurations.config import RABBITMQ_URL

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
print("Connected to RabbitMQ successfully!")
connection.close()