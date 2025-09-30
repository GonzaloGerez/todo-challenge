#!/bin/bash

# Setup script for Todo API project

echo "Setting up Todo API project..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
echo "Setting up environment file..."
cp env.example .env

# Create database (MySQL)
echo "Please create the MySQL database 'todo_db' manually:"
echo "CREATE DATABASE todo_db;"

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

echo "Setup complete!"
echo "To start the server, run: python manage.py runserver"

