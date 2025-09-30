#!/bin/bash

# Run script for Todo API project

echo "Starting Todo API server..."

# Activate virtual environment
source venv/bin/activate

# Run server
echo "Starting Django development server..."
python manage.py runserver

