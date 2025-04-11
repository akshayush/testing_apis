from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Dummy data for accounts
accounts_data = {
    1: ["Account1", "Account2"],
    2: ["Account3"],
    3: ["Account4", "Account5", "Account6"]
}

# Request model for customer ID
class Request(BaseModel):
    customer_id: int

@app.get("/")
def read_root():
    return {"message": "Hello, Railway!"}

@app.post("/get_accounts/")
def get_accounts(request: Request):
    print("Received request:", request.json())
    customer_id = request.customer_id
    if customer_id not in accounts_data:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    return {"customer_id": customer_id, "accounts": accounts_data[customer_id]}