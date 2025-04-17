# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the Python script
COPY ./bitcoin_sim.py /app/blockchain_server.py

# Install required packages
RUN pip install --no-cache-dir flask

# Expose port 5000
EXPOSE 5000

# Run the Flask application
CMD ["python", "blockchain_server.py"]
