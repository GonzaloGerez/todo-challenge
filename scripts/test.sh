#!/bin/bash

# Test script for Todo API project

echo "Running tests for Todo API project..."

# Activate virtual environment
source venv/bin/activate

# Run tests
echo "Running Django tests..."
python manage.py test

# Run with coverage (if coverage is installed)
if command -v coverage &> /dev/null; then
    echo "Running tests with coverage..."
    coverage run --source='.' manage.py test
    coverage report
    coverage html
fi

echo "Tests complete!"

