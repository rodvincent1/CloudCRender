from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import os
import random

app = FastAPI()

# Character schema
class Character(BaseModel):
    name: str
    age: int
    favorite_food: str
    quote: str

# Quote schema
class Quote(BaseModel):
    name: str
    quote: str

CHARACTER_FILE = "characters.csv"
QUOTE_FILE = "quotes.csv"

# Function to write data to a CSV file
def write_to_csv(file: str, headers: list, data: list):
    file_exists = os.path.isfile(file)
    
    with open(file, mode='a', newline='') as f:
        writer = csv.writer(f)
        
        # Write headers if the file is new
        if not file_exists:
            writer.writerow(headers)
        
        writer.writerow(data)

# POST: Create a new character@app.post("/create_character/")
async def create_character(character: Character):
    write_to_csv(CHARACTER_FILE, ["name", "age", "favorite_food", "quote"],
                 [character.name, character.age, character.favorite_food, character.quote])
    write_to_csv(QUOTE_FILE, ["name", "quote"], [character.name, character.quote])
    return {"msg": "Character created successfully!", "character": character}

# POST: Add a quote for an existing character
@app.post("/add_quote/")
async def add_quote(quote: Quote):
    if not os.path.exists(CHARACTER_FILE):
        raise HTTPException(status_code=404, detail="Character file not found.")
    
    with open(CHARACTER_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        if quote.name not in [row["name"] for row in reader]:
            raise HTTPException(status_code=404, detail="Character not found.")
    
    write_to_csv(QUOTE_FILE, ["name", "quote"], [quote.name, quote.quote])
    return {"msg": "Quote added successfully!", "quote": quote}

# GET: Retrieve all characters
@app.get("/characters/")
def get_characters():
    if not os.path.exists(CHARACTER_FILE):
        return {"msg": "No characters found."}
    
    with open(CHARACTER_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        characters = list(reader)
    
    return {"characters": characters}

# GET: Retrieve a character by name
@app.get("/characters/{name}")
async def get_character(name: str):
    if not os.path.exists(CHARACTER_FILE):
        raise HTTPException(status_code=404, detail="Character file not found.")
    
    with open(CHARACTER_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        characters = [row for row in reader if row["name"].lower() == name.lower()]
    
    if not characters:
        raise HTTPException(status_code=404, detail="Character not found.")
    
    return {"character": characters}

# GET: Retrieve a random quote
@app.get("/quote/")
def get_random_quote():
    if not os.path.exists(QUOTE_FILE):
        return {"msg": "No quotes available."}
    
    with open(QUOTE_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        quotes = list(reader)
    
    if not quotes:
        return {"msg": "No quotes available."}
    
    random_quote = random.choice(quotes)
    return {"quote": random_quote}
