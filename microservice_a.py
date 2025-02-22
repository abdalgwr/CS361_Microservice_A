import pika
import json


# Function to calculate average expenses
def calculate_average_expenses(data):
    # Example calculation logic
    expenses = data.get("expenses", [])
    if not expenses:
        return 0
    return sum(expenses) / len(expenses)


# Function to process the request
def process_request(request):
    request_type = request.get("type")
    data = request.get("data", {})

    if request_type == "average_expenses":
        average = calculate_average_expenses(data)
        return {
            "status": "success",
            "data": {
                "average_expenses": average,
                "period_start": data.get("period_start"),
                "period_end": data.get("period_end")
            }
        }
    else:
        return {
            "status": "error",
            "message": "Invalid request type"
        }


# RabbitMQ connection and queue setup
def start_microservice():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the request and response queues
    channel.queue_declare(queue='budget_requests')  # Queue for incoming requests
    channel.queue_declare(queue='budget_responses')  # Queue for outgoing responses

    # Callback function to handle incoming requests
    def callback(ch, method, properties, body):
        print(" [x] Received request:", body)

        # Parse the request
        request = json.loads(body)
        response = process_request(request)

        # Send the response back to the response queue
        channel.basic_publish(exchange='',
                              routing_key='budget_responses',
                              body=json.dumps(response))

        print(" [x] Sent response:", response)

    # Start consuming requests from the request queue
    channel.basic_consume(queue='budget_requests',
                          on_message_callback=callback,
                          auto_ack=True)

    print(' [*] Microservice A is waiting for requests. To exit press CTRL+C')
    channel.start_consuming()


# Start the microservice
if __name__ == "__main__":
    start_microservice()

