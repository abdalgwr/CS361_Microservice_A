### Requesting Data from Microservice A
To request data from Microservice A, send a JSON message to the RabbitMQ queue `budget_requests`. The message should include:
- `type`: The type of calculation (e.g., `"average_expenses"`).
- `data`: A JSON object with `month` and `year` dates.

**Example Request:**
```json
{
    "type": "average_expenses",
    "data": {
        "month": "february",
        "year": "2025"
    }
}
```

### Receiving Data from Microservice A
Microservice A will send a JSON response to the RabbitMQ queue `budget_responses`. The response will include:
- `status`: The status of the request (e.g., `"success"` or `"error"`).
- `data`: The calculated data (e.g., average expenses) along with the `month` and `year`.

**Example Response:**
```json
{
    "status": "success",
    "data": {
        "average_expenses": 130.0,
        "month": "february",
        "year": "2025"
    }
}
```

### UML Sequence Diagram
![UML Sequence Diagram](UMLA8.drawio.png)