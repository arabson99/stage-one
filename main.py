from fastapi import FastAPI, Query, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware
from typing import Any

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect(sum of divisors excluding itself equals the number)."""
    if n < 2:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is Armstrong number."""
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n


def get_fun_fact(n: int) -> str:
    """Get a fun fact about a number from Numbers API or return a custom fact for Armstrong numbers."""
    if armstrong(n):
        digits = [int(d) for d in str(n)]
        power = len(digits)
        sum_of_powers = " + ".join([f"{d}^{power}" for d in digits])
        return f"{n} is an Armstrong number because {sum_of_powers} = {n}"
    
    response = requests.get(f"http://numbersapi.com/{n}/math")
    try:
        return response.text if response.status_code == 200 else "No fun fact found."
    except Exception as e:
        return str(e)
    
@app.get("/api/classify-number")
async def classify_number(number: Any = Query(..., description="Number to classify")):
    """Classify a number and return its properties in JSON format."""
    try:
        # Check if the input is a valid integer
        try:
            number = int(number)
        except (ValueError, TypeError):
            # if conversion fails, return the required 400 Bad Request response
            raise HTTPException(
                status_code=400,
                detail={
                    "number": str(number),
                    "error": True
                }
            )
       
        
        # Classify the number
        prime = is_prime(number)
        perfect = is_perfect(number)
        armstrong = is_armstrong(number)
        odd = number % 2 != 0
        digit_sum = sum(int(d) for d in str(number))
        fun_fact = get_fun_fact(number)
        
        # Prepare the properties list
        properties = []
        if is_armstrong:
            properties.append("armstrong")
        properties.append("odd" if odd else "even")
        
        # Prepare the response
        return {
            "number": number,
            "is_prime": prime,
            "is_perfect": perfect,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)