FROM mcr.microsoft.com/devcontainers/python:1.2-3.12-bullseye

ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN python -m pip install --upgrade pip && pip --no-cache-dir install -r requirements.txt

# Copy the application code to the working directory
COPY . . 

# Expose the port on which the application will run
EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "log_conf.yaml", "--workers", "4"]
