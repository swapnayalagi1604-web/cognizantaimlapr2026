#rabbitmq connection
from contextlib import asynccontextmanager
from fastapi import FastAPI
import pika
import json
import threading
from driverapp.configurations.config import RABBITMQ_URL
'''
params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
print("Connected to RabbitMQ successfully!")
connection.close()
'''


def process_message(ch, method, properties, body):
    print("Received message:", body.decode())
    # Acknowledge the message after processing
    try:
       #read as json           
        data = json.loads(body.decode())
        print("Ride request details:", data)
        # Here you can add logic to handle the ride request, e.g., assign a driver, update database, etc.
        ch.basic_ack(delivery_tag=method.delivery_tag)  

    except Exception as e:
        print("Error processing message:", e)
        #reject and requeue the message for later processing
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    


def rabbitmq_consumer():
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    print("Connected to RabbitMQ successfully!")
    channel = connection.channel()
    channel.queue_declare(queue='ride_requests')
    #read one message at a time
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='ride_requests', on_message_callback=process_message)
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

@asynccontextmanager
async def start_up_event(app: FastAPI):
    #create background thread to consume messages from RabbitMQ
    threading.Thread(target=rabbitmq_consumer, daemon=True).start()
    print("RabbitMQ consumer thread started.")
    yield
    print("Shutting down RabbitMQ consumer thread.")

app=FastAPI(title="Driver App",
            description="API for drivers to manage rides",version="1.0",
            lifespan=start_up_event)

#check health of the application
@app.get("/health")
async def health_check():
    return {"status": "healthy"}