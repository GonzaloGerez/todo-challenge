@echo off
REM Docker setup script for Todo API project (Windows)

echo 🐳 Setting up Todo API with Docker...

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.example .env
    echo ✅ .env file created. Please edit it with your configurations.
)

REM Build and start services
echo 🔨 Building and starting services...
docker-compose up --build -d

REM Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Run migrations
echo 🗄️ Running database migrations...
docker-compose exec web python manage.py migrate

REM Create superuser (optional)
echo 👤 Creating superuser...
docker-compose exec web python manage.py createsuperuser --noinput --email admin@example.com --username admin 2>nul || echo Superuser already exists or creation failed

echo ✅ Setup complete!
echo.
echo 🌐 Services available at:
echo    - API: http://localhost:8000
echo    - API Health: http://localhost:8000/api/health/
echo    - Admin: http://localhost:8000/admin/
echo    - phpMyAdmin: http://localhost:8080
echo.
echo 📋 Useful commands:
echo    - View logs: docker-compose logs -f
echo    - Stop services: docker-compose down
echo    - Restart services: docker-compose restart
echo    - Access web container: docker-compose exec web bash
echo    - Access database: docker-compose exec db mysql -u todo_user -p todo_db
pause

