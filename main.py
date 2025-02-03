from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Optional

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


async def get_fun_fact(n: int) -> str:
    """Fetch a fun fact asynchronously to avoid slow responses."""
    url = f"http://numbersapi.com/{n}/math"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for HTTP error responses
            return response.text
    except httpx.HTTPStatusError:
        return "Error: Unable to fetch fun fact (invalid response from API)."
    except httpx.RequestError:
        return "Error: Could not reach the Numbers API."
    
@app.get("/api/classify-number")
async def classify_number(number: Optional[Any] = Query(None, description="Number to classify")):
    """Classify a number and return its properties in JSON format."""
    try:
        # Check if the input is a valid integer
        try:
            number = int(number)
        except (ValueError, TypeError):
            # if conversion fails, return the required 400 Bad Request response
            return  JSONResponse(
                content={"number": str(number), "error": True },
                status_code=400
            )
    
        
        # Classify the number
        prime = is_prime(number)
        perfect = is_perfect(number)
        armstrong = is_armstrong(number)
        odd = number % 2 != 0
        digit_sum = sum(int(d) for d in str(number))
        fun_fact = await get_fun_fact(number)
        
        # Prepare the properties list
        properties = []
        if armstrong:
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
        return  JSONResponse(
                content={"number": str(number), "error": True },
                status_code=400
            )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)