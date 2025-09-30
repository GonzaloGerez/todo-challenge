@echo off
REM Test script for Todo API project (Windows)

echo Running tests for Todo API project...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run tests
echo Running Django tests...
python manage.py test

REM Run with coverage (if coverage is installed)
where coverage >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Running tests with coverage...
    coverage run --source='.' manage.py test
    coverage report
    coverage html
)

echo Tests complete!
pause

