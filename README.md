# Todo API - Django REST Framework

Una API REST desarrollada con Django que implementa un sistema de autenticación por email/password y utiliza una arquitectura de capas bien definida.

## Arquitectura del Proyecto

El proyecto sigue el patrón de arquitectura en capas:

```
API Layer (Views) → Service Layer → Repository Layer → Database
```

### Estructura de Capas

1. **API Layer (Views)**: Maneja las peticiones HTTP y respuestas
2. **Service Layer**: Contiene la lógica de negocio
3. **Repository Layer**: Administra las entidades de la base de datos y operaciones CRUD
4. **Database**: MySQL como base de datos principal

## Características

- ✅ Autenticación por email/password
- ✅ Modelo de usuario personalizado
- ✅ Sistema de gestión de tareas
- ✅ Arquitectura en capas (API → Servicios → Repositorios)
- ✅ Base de datos MySQL
- ✅ Django REST Framework
- ✅ JWT Tokens con duración de 1 hora
- ✅ Validación de datos
- ✅ Manejo de errores estandarizado
- ✅ Dockerización completa
- ✅ Organización modular con carpeta `src/`

## Instalación

### Prerrequisitos

- Python 3.8+
- MySQL 5.7+
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd todo-challenge
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   # En Windows
   .\venv\Scripts\Activate.ps1
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp env.example .env
   ```
   
   Editar el archivo `.env` con tus configuraciones:
   ```env
   DB_NAME=todo_db
   DB_USER=root
   DB_PASSWORD=tu_password
   DB_HOST=localhost
   DB_PORT=3306
   SECRET_KEY=tu-secret-key-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Configurar base de datos MySQL**
   - Crear la base de datos: `CREATE DATABASE todo_db;`

6. **Ejecutar migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

## Uso de la API

### Endpoints Disponibles

#### Autenticación

- **POST** `/api/auth/register/` - Registrar nuevo usuario
- **POST** `/api/auth/login/` - Iniciar sesión (devuelve JWT token)

#### Tareas (Requieren autenticación)

- **POST** `/api/tasks/` - Crear nueva tarea
- **PUT** `/api/tasks/{id}/status/` - Actualizar estado de tarea
- **GET** `/api/tasks/search/` - Buscar tareas (por detalle y/o fecha)

#### General

- **GET** `/api/health/` - Health check

### Ejemplos de Uso

#### 1. Registrar Usuario

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

#### 2. Iniciar Sesión

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "password123"
  }'
```

#### 3. Crear Tarea (Requiere autenticación)

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu-jwt-token-aqui" \
  -d '{
    "detail": "Completar documentación del proyecto"
  }'
```

#### 4. Actualizar Estado de Tarea

```bash
curl -X PUT http://localhost:8000/api/tasks/1/status/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu-jwt-token-aqui" \
  -d '{
    "status": "completed"
  }'
```

#### 5. Buscar Tareas

```bash
# Buscar todas las tareas
curl -X GET http://localhost:8000/api/tasks/search/ \
  -H "Authorization: Bearer tu-jwt-token-aqui"

# Buscar por detalle
curl -X GET "http://localhost:8000/api/tasks/search/?detail=documentación" \
  -H "Authorization: Bearer tu-jwt-token-aqui"

# Buscar por fecha
curl -X GET "http://localhost:8000/api/tasks/search/?created_date=2025-09-28" \
  -H "Authorization: Bearer tu-jwt-token-aqui"
```

#### 6. Health Check

```bash
curl -X GET http://localhost:8000/api/health/
```

### JWT Tokens

El sistema utiliza JWT (JSON Web Tokens) para la autenticación:

- **Access Token**: Válido por 1 hora
- **Refresh Token**: Válido por 7 días
- **Header**: `Authorization: Bearer <token>`

#### Respuesta del Login

```json
{
  "success": true,
  "message": "Authentication successful",
  "data": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 3600
  }
}
```

## Estructura del Proyecto

```
todo-challenge/
├── src/                    # Módulos funcionales del proyecto
│   ├── authentication/     # App de autenticación
│   │   ├── models.py       # Modelo de usuario personalizado
│   │   ├── views.py        # Vistas de la API
│   │   ├── urls.py         # URLs de autenticación
│   │   └── admin.py        # Configuración del admin
│   ├── core/               # App principal con funcionalidades de tareas
│   │   ├── repositories/   # Capa de repositorios
│   │   │   ├── base_repository.py
│   │   │   ├── user_repository.py
│   │   │   └── task_repository.py
│   │   ├── services/       # Capa de servicios
│   │   │   ├── base_service.py
│   │   │   ├── user_service.py
│   │   │   └── task_service.py
│   │   ├── models.py       # Modelos de datos
│   │   ├── views.py        # Vistas de la API
│   │   └── urls.py         # URLs principales
│   └── todo_api/           # Configuración del proyecto Django
│       ├── settings.py     # Configuraciones
│       ├── urls.py         # URLs principales
│       ├── wsgi.py         # WSGI configuration
│       └── asgi.py         # ASGI configuration
├── staticfiles/            # Archivos estáticos recopilados
├── venv/                   # Entorno virtual (no incluido en git)
├── requirements.txt        # Dependencias del proyecto
├── env.example            # Variables de entorno de ejemplo
├── docker-compose.yml     # Configuración de Docker Compose
├── Dockerfile             # Configuración del contenedor Django
├── manage.py              # Script de administración de Django
└── README.md              # Este archivo
```

## Patrones de Diseño Implementados

### Repository Pattern
- `BaseRepository`: Clase base con operaciones CRUD comunes
- `UserRepository`: Repositorio específico para usuarios
- `TaskRepository`: Repositorio específico para tareas

### Service Pattern
- `BaseService`: Clase base con validaciones comunes
- `UserService`: Servicio con lógica de negocio para usuarios
- `TaskService`: Servicio con lógica de negocio para tareas

### Dependency Injection
- Los servicios utilizan repositorios como dependencias
- Fácil testing y mantenimiento

### Organización Modular
- **Carpeta `src/`**: Contiene todos los módulos funcionales del proyecto
- **Separación clara**: Configuración Django vs. lógica de negocio
- **Escalabilidad**: Fácil agregar nuevas funcionalidades sin afectar la estructura base

## Configuración de Base de Datos

El proyecto está configurado para usar MySQL. Asegúrate de tener MySQL instalado y configurado antes de ejecutar las migraciones.

## 🐳 Dockerización

El proyecto incluye configuración completa de Docker para facilitar el despliegue y desarrollo.

### Servicios Docker

- **MySQL 8.0**: Base de datos en el puerto 3306
- **Django API**: Aplicación en el puerto 8000
- **phpMyAdmin**: Interfaz web para MySQL en el puerto 8080

### Opción 1: Usando el script de configuración (Recomendado)

**Linux/Mac:**
```bash
chmod +x scripts/docker-setup.sh
./scripts/docker-setup.sh
```

**Windows:**
```cmd
scripts\docker-setup.bat
```

### Opción 2: Comandos manuales

```bash
# Construir y levantar todos los servicios
docker-compose up --build -d

# Ver logs
docker-compose logs -f

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Parar servicios
docker-compose down
```

### Servicios disponibles con Docker:

- **API**: http://localhost:8000
- **API Health Check**: http://localhost:8000/api/health/
- **Admin Panel**: http://localhost:8000/admin/
- **phpMyAdmin**: http://localhost:8080
- **MySQL**: localhost:3306

### Comandos útiles de Docker:

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Acceder al contenedor de la aplicación
docker-compose exec web bash

# Acceder a la base de datos
docker-compose exec db mysql -u todo_user -p todo_db

# Reiniciar un servicio específico
docker-compose restart web

# Ver el estado de los contenedores
docker-compose ps

# Limpiar volúmenes (¡CUIDADO! Esto borra la base de datos)
docker-compose down -v
```


## Desarrollo

### Agregar Nuevas Funcionalidades

1. **Crear modelo** en la app correspondiente
2. **Crear repositorio** en `core/repositories/`
3. **Crear servicio** en `core/services/`
4. **Crear vistas** en la app correspondiente
5. **Agregar URLs** correspondientes

### Testing

El proyecto incluye una suite completa de tests usando pytest:

#### Estructura de Tests
```
tests/
├── unit/                    # Tests unitarios
│   ├── repositories/        # Tests de repositorios
│   └── services/           # Tests de servicios
├── integration/            # Tests de integración
│   ├── services/           # Tests de servicios con BD
│   └── api/               # Tests de endpoints
├── factories.py           # Factories para datos de prueba
└── conftest.py           # Configuración de pytest
```

#### Ejecutar Tests

```bash
# Instalar dependencias de testing
pip install -r requirements.txt

# Ejecutar todos los tests
python -m pytest

# Ejecutar solo tests unitarios
python -m pytest -m unit

# Ejecutar solo tests de integración
python -m pytest -m integration

# Ejecutar con cobertura
python -m pytest --cov=src --cov-report=html

# Usar el script de testing
python scripts/run_tests.py --coverage
```

#### Cobertura de Tests
- **Tests Unitarios**: Repositorios y servicios con mocks
- **Tests de Integración**: Servicios con BD real y endpoints API
- **Factory Boy**: Generación de datos de prueba
- **Pytest**: Framework de testing con marcadores y fixtures

Para más detalles, consulta [tests/README.md](tests/README.md).


## Herramientas de Desarrollo

Este proyecto fue desarrollado utilizando **Cursor** como IDE principal para evaluar la eficiencia y rendimiento de la herramienta en el desarrollo de aplicaciones Django con arquitectura en capas. La experiencia de desarrollo incluyó:

- **Generación de código** automatizada y contextual
- **Refactoring** inteligente y mantenimiento de consistencia
- **Debugging** y resolución de problemas
- **Testing** automatizado con pytest
- **Dockerización** y configuración de entornos
- **Documentación** técnica detallada

### Resultados de la Evaluación

- ✅ **Desarrollo ágil**: Implementación completa en tiempo récord
- ✅ **Calidad de código**: Arquitectura limpia y bien estructurada
- ✅ **Testing robusto**: 74 tests con 77% de cobertura
- ✅ **Documentación completa**: README detallado y comentarios en código
- ✅ **Dockerización**: Entorno de desarrollo y producción containerizado

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.