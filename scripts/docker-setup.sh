#!/bin/bash

# Docker setup script for Todo API project

echo "🐳 Setting up Todo API with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created. Please edit it with your configurations."
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🗄️ Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser (optional)
echo "👤 Creating superuser..."
docker-compose exec web python manage.py createsuperuser --noinput --email admin@example.com --username admin || echo "Superuser already exists or creation failed"

echo "✅ Setup complete!"
echo ""
echo "🌐 Services available at:"
echo "   - API: http://localhost:8000"
echo "   - API Health: http://localhost:8000/api/health/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - phpMyAdmin: http://localhost:8080"
echo ""
echo "📋 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo "   - Access web container: docker-compose exec web bash"
echo "   - Access database: docker-compose exec db mysql -u todo_user -p todo_db"

