# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Initialize the database
RUN python app/db.py

# Expose ports for both the API (8000) and Frontend (8080)
EXPOSE 8000 8080

# Make the start script executable
RUN chmod +x start.sh

# Run the start script when the container launches
CMD ["./start.sh"]
