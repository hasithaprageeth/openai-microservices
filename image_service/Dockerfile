FROM python:3.9-slim-buster

# Install build essentials
#RUN apt-get clean && apt-get -y update

# Set work directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
