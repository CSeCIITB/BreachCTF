# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port if needed (optional)
# EXPOSE 8000

# Define environment variables if desired (can also be provided at runtime)
# ENV WEBHOOK_URL=<your_webhook_url>
# ENV CTFD_URL=<your_ctfd_url>
# ENV CTFD_ACCESS_TOKEN=<your_ctfd_access_token>

# Run the application:
CMD ["python", "first-blood.py"]

