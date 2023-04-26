FROM python:3.9-slim-buster

# Install dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Set work directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
