
# Number Classifier API

## Description
This FastAPI application provides an API to classify numbers and check their properties, such as prime, perfect, Armstrong, and even/odd. The API also provides a fun fact about the number when available. 

### Properties Check:
- **Prime:** Determines if the number is prime.
- **Perfect:** Determines if the number is perfect (sum of divisors excluding itself equals the number).
- **Armstrong:** Determines if the number is an Armstrong number, and provides a mathematical explanation.
- **Even/Odd:** Classifies the number as either even or odd.
- **Digit Sum:** Calculates the sum of the digits of the number.

### Fun Fact:
- If the number is Armstrong, the API will provide a detailed explanation of why it's Armstrong.
- If the number is not Armstrong, the API will fetch a general fun fact from the Numbers API.

## Features
- CORS support for cross-origin requests.
- Detailed classification of numbers (prime, perfect, Armstrong, even/odd).
- Fun facts from the Numbers API, with fallback handling for unavailable facts.

## Installation

### Prerequisites
Ensure you have Python 3.8+ installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arabson99/stage-one.git
   cd stage-one
   ```

2. **Install dependencies:**
   Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   pip install -r requirements.txt
   ```

3. **Install required Python packages:**
   - FastAPI
   - uvicorn
   - requests

4. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API:**
   The API will be available at `http://127.0.0.1:8000`. You can visit the automatically generated Swagger UI at `http://127.0.0.1:8000/docs` to interact with the API.

## API Endpoints

### `/api/classify-number`
#### Method: `GET`

#### Query Parameters:
- **number**: The number to classify. This parameter is required and should be an integer.

#### Example Request:
```bash
GET http://127.0.0.1:8000/api/classify-number?number=371
```

#### Response (200 OK):
```json
{
  "number": 371,
  "is_prime": false,
  "is_perfect": false,
  "properties": ["armstrong", "odd"],
  "digit_sum": 11,
  "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

#### Response (400 Bad Request):
If the number is invalid or cannot be converted to an integer, you will receive a `400` response:
```json
{
  "number": "alphabet",
  "error": true
}
```

## Error Handling
- If the number cannot be parsed as an integer, a `400 Bad Request` error is returned with the number and error details.
- If an unexpected error occurs, a generic error message is returned.

## License
MIT License

## Author
Abubakar, Abdulazeez Usman
[Github](https://github.com/arabson99/)

