@echo off
REM Setup script for Todo API project (Windows)

echo Setting up Todo API project...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Copy environment file
echo Setting up environment file...
copy env.example .env

REM Create database (MySQL)
echo Please create the MySQL database 'todo_db' manually:
echo CREATE DATABASE todo_db;

REM Run migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo Creating superuser...
python manage.py createsuperuser

echo Setup complete!
echo To start the server, run: python manage.py runserver
pause

