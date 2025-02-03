FROM python:3.11-slim-buster

# Set the working directory
WORKDIR /app

# Create a data directory
RUN mkdir -p /app/data

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./src .

# Command to run the application
CMD ["fastapi", "run", "./server.py", "--port", "8000"]