from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random 

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

# Request model for customer ID
class AccountRequest(BaseModel):
    account_number: str
    customer_id : int


class PayeeRequest(BaseModel):
    customer_id: int
    payee_name: str
    account_number: str 
    sort_code: str

class TransferRequest(BaseModel):
    customer_id: int
    account_from: str
    account_to: str
    amount: float


@app.get("/")
def read_root():
    return {"message": "Hello, Railway!"}

@app.post("/get_accounts")
def get_accounts(request: Request):
    print("Received request:", request.json())
    customer_id = request.customer_id
    if customer_id not in accounts_data:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    return {"customer_id": customer_id, "accounts": accounts_data[customer_id]}


@app.post("/add_payee")
def add_payee(request: PayeeRequest):
    print(f"Request received: {request.json()}")
    customer_id = request.customer_id
    payee_name = request.payee_name
    account_number = request.account_number
    sort_code = request.sort_code
    if customer_id not in accounts_data:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    return ("Details added for the customer")


@app.post("/transfer_funds")
def transfer_funds(request: Request):
    print(f"Request received: {request.json()}")
    customer_id = request.customer_id
    if customer_id not in accounts_data:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    accounts= accounts_data.get(customer_id, [])
    if not accounts:
        raise HTTPException(status_code=404, detail="Customer ID not found or no accounts available")
    fulfilment_api={"api":"/get_transfer_fulfilment",
    "method":"POST", "headers": {"Content-Type": "application/json",},
    "parameters": "customer_id,account_from,account_to,amount"}
    balance_enquiry_api={"api":"/enquire_balance",
    "method":"POST", "headers": {"Content-Type": "application/json",},  
    "parameters": "account_number,customer_id"}
    return {"fulfilment_api": fulfilment_api, "balance_enquiry_api": balance_enquiry_api,"accounts": accounts, "customer_id": customer_id, "message": "Transfer funds API called successfully"}


@app.post("/get_transfer_fulfilment")
def get_transfer_fulfilment(request: Request):
    print(f"Request received: {request.json()}")
    customer_id = request.customer_id
    account_from=request.account_from
    account_to=request.account_to
    amount=request.amount
    if customer_id not in accounts_data:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    accounts= accounts_data.get(customer_id, [])
    if not accounts:
        raise HTTPException(status_code=404, detail="Customer ID not found or no accounts available")
    
@app.post("/enquire_balance")
def enquire_balance(request: AccountRequest):
    print(f"Request received: {request.json()}")
    customer_id = request.customer_id
    account_number = request.account_number
    if customer_id not in accounts_data:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    accounts= accounts_data.get(customer_id, [])
    if not accounts:
        raise HTTPException(status_code=404, detail="Customer ID not found or no accounts available")    
    random_number = random.randrange(1000, 10000 + 0, 100)
    return random_number  # Dummy balance for the sake of example