FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set environment variable
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=ON"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# Command to run the server
CMD ["python3", "./server.py"]
