import pika
import json

with open('data.json', 'r') as file:
    data = json.load(file)


# Function to calculate average expenses
def calculate_average_expenses(month, year):
    try:
        # Extract expenses for the specified month and year
        expenses = data["years"][year]["months"][month]["expenses"]
        if not expenses:
            return 0
        # Calculate the average
        total = sum(item["amount"] for item in expenses)
        return total / len(expenses)
    except KeyError:
        return 0  # Return 0 if the specified month or year is not found


# Function to process the request
def process_request(request):
    request_type = request.get("type")
    data = request.get("data", {})

    if request_type == "average_expenses":
        month = data.get("month")
        year = data.get("year")
        average = calculate_average_expenses(month, year)
        return {
            "status": "success",
            "data": {
                "average_expenses": average,
                "month": month,
                "year": year
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

        request = json.loads(body)
        response = process_request(request)

        channel.basic_publish(exchange='',
                              routing_key='budget_responses',
                              body=json.dumps(response))

        print(" [x] Sent response:", response)

    channel.basic_consume(queue='budget_requests',
                          on_message_callback=callback,
                          auto_ack=True)

    print(' [*] Microservice A is waiting for requests. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    start_microservice()

