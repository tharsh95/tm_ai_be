from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB connection details from environment variables
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Create MongoDB client with proper Atlas connection parameters
client = MongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=5000,  # 5 seconds timeout
    retryWrites=True,
    w="majority",
    tlsAllowInvalidCertificates=True
)

# Test the connection
try:
    # The ismaster command is cheap and does not require auth
    client.admin.command('ismaster')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {e}")
    raise

if DATABASE_NAME is None:
    raise ValueError("DATABASE_NAME environment variable is not set")

db = client[DATABASE_NAME] 