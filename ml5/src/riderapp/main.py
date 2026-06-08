#rabbitmq connection
from fastapi import FastAPI
import pika

from riderapp.configurations.config import RABBITMQ_URL
'''
params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
print("Connected to RabbitMQ successfully!")
connection.close()
'''
app=FastAPI(title="Rider App",description="API for riders to request rides",version="1.0")

def publish_rider_request(rider_mobile_no, pickup_location, dropoff_location):
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    # Declare the queue to ensure it exists
    channel.queue_declare(queue='ride_requests')
    
    # Create the message
    message = f"{rider_mobile_no}:{pickup_location}:{dropoff_location}"
    
    # Publish the message to the queue
    channel.basic_publish(exchange='', routing_key='ride_requests', body=message)
    
    print(f"Published ride request: {message}")
    
    # Close the connection
    connection.close()

@app.post("/request_ride")
def send_ride_request(rider_mobile_no: str, pickup_location: str, dropoff_location: str):
    publish_rider_request(rider_mobile_no, pickup_location, dropoff_location)
    return {"message": "Ride request sent successfully!"}