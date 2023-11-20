# Use the official Python image for Python 3.11
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ENV CMAKE_ARGS="-DLLAMA_CUBLAS=on"

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the server
CMD ["python", "./server.py"]

# Expose the port your app runs on
EXPOSE 8080