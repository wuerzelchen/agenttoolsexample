from msal import ConfidentialClientApplication
from fastapi import FastAPI
# dotenv
from dotenv import load_dotenv
import os
load_dotenv()
app = FastAPI()

client = ConfidentialClientApplication(
    client_id="332551fa-2cc8-4511-8e9c-cfbaf9451565",
    client_credential=os.getenv("CLIENT_SECRET"),
    authority="https://login.microsoftonline.com/1073630d-9e47-407e-b1be-a97cc5f7b790"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

# secured get_info endpoint


@app.get("/get_info")
async def get_info():
    # Mocked list of machines
    machines = [
        {
            "id": "machine-001",
            "status": "running",
            "location": "Berlin",
            "current_operator": "Alice",
            "temperature_celsius": 68.5
        },
        {
            "id": "machine-002",
            "status": "stopped",
            "location": "Munich",
            "current_operator": "Bob",
            "temperature_celsius": 22.1
        },
        {
            "id": "machine-003",
            "status": "maintenance",
            "location": "Hamburg",
            "current_operator": "Charlie",
            "temperature_celsius": 35.0
        }
    ]
    return {"machines": machines}
