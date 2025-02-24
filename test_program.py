import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='budget_requests')
channel.queue_declare(queue='budget_responses')

request_message = {
    "type": "average_expenses",
    "data": {
        "month": "february",
        "year": "2025"
    }
}

channel.basic_publish(exchange='',
                      routing_key='budget_requests',
                      body=json.dumps(request_message))

print(" \n[x] Sent request to RabbitMQ:", request_message)


# Define a callback function to process the response
def callback(ch, method, properties, body):
    response = json.loads(body)
    print(" \n[x] Received response from RabbitMQ:", response)
    connection.close()


channel.basic_consume(queue='budget_responses',
                      on_message_callback=callback,
                      auto_ack=True)

print(' \n[*] Waiting for responses. To exit press CTRL+C')
channel.start_consuming()

