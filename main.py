from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import csv
import os

app = FastAPI()

# Pydantic model to validate the data for creating users
class UserCreate(BaseModel):
    user_id: int
    username: str

# Function to write user data to the CSV file
def write_to_csv(user_id: int, username: str):
    csv_file = "users_data.csv"
    file_exists = os.path.isfile(csv_file)
    
    # Print data to terminal for debugging
    print(f"Writing data to {csv_file}: user_id={user_id}, username={username}")
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # If the file doesn't exist, write the headers
        if not file_exists:
            writer.writerow(["user_id", "username"])
        
        # Write the new user data
        writer.writerow([user_id, username])

# POST endpoint to create a new user and save the data to CSV
@app.post("/create_user/")
async def create_user(user_data: UserCreate):
    # Print received data for debugging
    print(f"Received data: user_id={user_data.user_id}, username={user_data.username}")
    
    user_id = user_data.user_id
    username = user_data.username
    
    # Write the received data to the CSV file
    write_to_csv(user_id, username)
    
    # Return success message with the received data
    return {
        "msg": "We got data successfully and saved it to CSV",
        "user_id": user_id,
        "username": username,
    }

# GET endpoint to retrieve all users from the CSV file
@app.get("/get_users/")
def get_users():
    csv_file = "users_data.csv"
    users = []

    # If the file exists, read the user data
    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)

    return {"users": users}

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.4", port=8000)
