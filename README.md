# FastAPI MongoDB Example

A simple FastAPI application with MongoDB integration using Pydantic models.

## Prerequisites

- Python 3.8+
- MongoDB installed and running locally
- Virtual environment (recommended)

## Setup

1. Clone the repository
2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure MongoDB is running locally on port 27017

5. Create a `.env` file with the following content:
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=fastapi_db
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Endpoints

- `GET /`: Welcome message
- `POST /items/`: Create a new item
- `GET /items/`: Get all items
- `GET /items/{item_id}`: Get a specific item by ID 