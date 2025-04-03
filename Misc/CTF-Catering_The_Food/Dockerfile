FROM gcc:10

# Install dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    bubblewrap \
    bash \
    libcap2 \
    libseccomp2 \
    procps \
    pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the web API and runner scripts.
COPY WEB_API.py /app/WEB_API.py
COPY run_submission.sh /run_submission.sh
COPY testcases/ /testcases/
RUN pip install flask

# Copy the static directory containing the question PDF.
COPY static/ /app/static/

# Ensure static files are readable by the runner user.
RUN useradd -m runner
RUN chown -R runner:runner /app/static

# Make sure the runner script is executable.
RUN chmod +x /run_submission.sh

# Create a directory for submissions and change ownership to 'runner'
RUN mkdir -p /tmp/submissions && chown runner:runner /tmp/submissions

# Create a non-privileged user.

# Switch to the non-privileged user.
USER runner

# Set the working directory.
WORKDIR /app

# Expose the port for the Flask API.
EXPOSE 5050

# Start the Flask API.
CMD ["python3", "WEB_API.py"]
