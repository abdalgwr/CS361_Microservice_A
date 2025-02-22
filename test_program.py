import pika
import json

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the request and response queues
channel.queue_declare(queue='budget_requests')
channel.queue_declare(queue='budget_responses')

# Prepare the request message
request_message = {
    "type": "average_expenses",
    "data": {
        "period_start": "2025-01-01",
        "period_end": "2025-01-31"
    }
}

# Send the request to the queue
channel.basic_publish(exchange='',
                      routing_key='budget_requests',
                      body=json.dumps(request_message))

print(" [x] Sent request to RabbitMQ:", request_message)


# Define a callback function to process the response
def callback(ch, method, properties, body):
    response = json.loads(body)
    print(" [x] Received response from RabbitMQ:", response)
    connection.close()


# Consume the response from the queue
channel.basic_consume(queue='budget_responses',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for responses. To exit press CTRL+C')
channel.start_consuming()