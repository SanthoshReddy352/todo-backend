# app/config.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (optional)
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "todo"  # Your database name
USERS_COLLECTION = "users"  # Your users collection

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
users_collection = db[USERS_COLLECTION]

print(f"Connected to MongoDB database: {DATABASE_NAME}, collection: {USERS_COLLECTION}")
