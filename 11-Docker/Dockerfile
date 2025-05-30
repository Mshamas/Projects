# Use an official Python runtime as the base image

FROM --platform=linux/amd64 python:3.10.13

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code to the working directory
COPY model.pkl ./
COPY docker_api.py ./
COPY requirements.txt ./
COPY train.csv ./
COPY model2.pkl ./


# Expose port 80 for the FastAPI application
EXPOSE 80
ENV PORT=80

# Run the FastAPI application using Uvicorn when the container starts
CMD ["python", "docker_api.py"]
