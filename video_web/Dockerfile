# Dockerfile

# Use official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install the required dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code
COPY . /app/

# Install libpq-dev
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install django
RUN pip install psycopg2-binary

# Run database migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
