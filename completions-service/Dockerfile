FROM python:3.9-slim-buster

# Set work directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Expose port 8001 for Gunicorn
EXPOSE 80

# Run the application using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
