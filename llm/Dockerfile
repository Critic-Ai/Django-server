# Use the official Python image for Python 3.11
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ENV FORCE_CMAKE=1

ENV CMAKE_ARGS="-DLLAMA_CUBLAS=on"


# Install project dependencies

RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

# Command to run the server
CMD ["python", "./server.py"]