# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/

# Expose the port that FastAPI is running on (default is 8000)
EXPOSE 8000

# Command to start your FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
