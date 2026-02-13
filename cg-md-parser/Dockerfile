# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script code into the container
COPY cg-md_tool.py .

# Create a directory for input/output to ensure mount points exist (optional but good practice)
RUN mkdir -p /app/cg_md_output

# Define environment variable for Ollama
# On Windows/Mac with Docker Desktop, 'host.docker.internal' resolves to the host machine.
# On Linux, you might need to use --network="host" or the host's actual IP.
ENV OLLAMA_URL=http://host.docker.internal:11434/api/generate

# Run the script when the container launches
ENTRYPOINT ["python", "cg-md_tool.py"]
