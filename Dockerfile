# Use a Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install email-validator pydantic-settings

# Copy the rest of the server application files
COPY . .

# Expose the port the server runs on
EXPOSE 8000

# Set environment variables
ENV ENV_VAR_NAME=env_value

# Command to run the server application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 