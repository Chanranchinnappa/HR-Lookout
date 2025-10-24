# HR-Lookout - Enterprise HRIS Platform

A modern, scalable Human Resources Information System built with microservices architecture.

**Version**: 1.0.0  
**Status**: Phase 2 Complete ✅  
**Last Updated**: October 25, 2025

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Services](#services)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)

---

## 🎯 Overview

HR-Lookout is an enterprise-grade Human Resources Information System featuring:

- **Employee Management** - Complete employee lifecycle management
- **Organization Hierarchy** - Multi-level organizational structure
- **Department Management** - Department creation and assignment
- **Document Management** - Secure document storage and retrieval
- **Audit Logging** - Complete audit trail in MongoDB
- **GraphQL & REST APIs** - Flexible API access
- **Microservices Architecture** - Scalable, distributed system

### Key Features

✅ REST & GraphQL APIs  
✅ Real-time health monitoring  
✅ Multi-database architecture  
✅ Docker containerization  
✅ Audit logging for all operations  
✅ Organizational hierarchy visualization  
✅ Role-based access control (framework ready)  
✅ Document management system  

---

## 🏗️ Architecture

### Technology Stack

**Backend**
- Django 5.0.7
- Django REST Framework 3.15.2
- Graphene-Django 3.2.2
- Python 3.11

**Databases**
- PostgreSQL 15 (Primary data)
- MongoDB 7 (Audit logs)
- Neo4j 5 (Org charts)
- Redis 7 (Cache & sessions)

**Infrastructure**
- Keycloak 23 (Authentication)
- MinIO (Object storage)
- Traefik 2.10 (API Gateway)
- Docker & Docker Compose

### System Architecture

┌─────────────────────────────────────────────────────────┐
│ Traefik (API Gateway) │
│ Port 80, 8080 │
└────────────────────┬────────────────────────────────────┘
│
┌────────────┴────────────┐
│ │
▼ ▼
┌──────────────┐ ┌──────────────┐
│ Keycloak │ │ hr-core │
│ Port 8180 │◄─────────│ Port 8001 │
└──────────────┘ └──────┬───────┘
│
┌────────────┼────────────┐
│ │ │
▼ ▼ ▼
┌─────────────┐ ┌─────────┐ ┌─────────┐
│ PostgreSQL │ │ MongoDB │ │ Neo4j │
│ Port 5432 │ │Port 27017│ │Port 7474│
└─────────────┘ └─────────┘ └─────────┘
│
▼
┌─────────────┐
│ Redis │
│ Port 6379 │
└─────────────┘
│
▼
┌─────────────┐
│ MinIO │
│ Port 9000-1 │
└─────────────┘


---

## 🚀 Quick Start

### Prerequisites

**Required**:
- Docker Desktop 4.0+ (Windows/Mac) or Docker Engine 20.0+ (Linux)
- Docker Compose v2.0+
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space

**Optional**:
- Git 2.0+
- VS Code or preferred IDE

### Installation Steps

**1. Clone or Navigate to Project**
cd C:\Users\YourName\Projects\HR-Lookout

**2. Start All Services**
Start infrastructure
docker-compose up -d

Verify all services are running
docker-compose ps


**3. Run Database Migrations**
Apply Django migrations
docker-compose exec hr-core python manage.py migrate

Verify migrations
docker-compose exec hr-core python manage.py showmigrations


**4. Create Admin User**
docker-compose exec hr-core python manage.py createsuperuser

Username: admin
Email: admin@hrlookout.local
Password: (choose secure password)


**5. Access the Application**

Open your browser:
- **Django Admin**: http://localhost:8001/admin/
- **GraphQL Playground**: http://localhost:8001/graphql/
- **REST API**: http://localhost:8001/api/v1/

---

## 📡 API Documentation

### REST API Endpoints

**Base URL**: `http://localhost:8001/api/v1/`

#### Organizations

GET /api/v1/organizations/ # List all organizations
POST /api/v1/organizations/ # Create organization
GET /api/v1/organizations/{id}/ # Get organization details
PUT /api/v1/organizations/{id}/ # Update organization (full)
PATCH /api/v1/organizations/{id}/ # Update organization (partial)
DELETE /api/v1/organizations/{id}/ # Delete organization
GET /api/v1/organizations/{id}/departments/ # Get org departments
GET /api/v1/organizations/{id}/employees/ # Get org employees


**Example: Create Organization**
curl -X POST http://localhost:8001/api/v1/organizations/
-H "Content-Type: application/json"
-d '{
"name": "Tech Corp",
"legal_name": "Tech Corp Inc.",
"email": "info@techcorp.com",
"tax_id": "12-3456789",
"address_line1": "123 Main St",
"city": "San Francisco",
"state": "CA",
"postal_code": "94102",
"country": "United States",
"fiscal_year_start": "2024-01-01",
"currency": "USD",
"timezone": "America/Los_Angeles"
}'


#### Employees
GET /api/v1/employees/ # List all employees
POST /api/v1/employees/ # Create employee
GET /api/v1/employees/{id}/ # Get employee details
PUT /api/v1/employees/{id}/ # Update employee (full)
PATCH /api/v1/employees/{id}/ # Update employee (partial)
DELETE /api/v1/employees/{id}/ # Soft delete (mark terminated)
GET /api/v1/employees/me/ # Get current user's profile
GET /api/v1/employees/search/?q=John # Search employees
GET /api/v1/employees/{id}/documents/ # Get employee documents


**Example: Create Employee**
curl -X POST http://localhost:8001/api/v1/employees/
-H "Content-Type: application/json"
-d '{
"employee_id": "EMP001",
"first_name": "John",
"last_name": "Doe",
"email": "john.doe@techcorp.com",
"phone": "+14155551234",
"organization": 1,
"department": 1,
"job_title": "Senior Software Engineer",
"employment_status": "ACTIVE",
"employment_type": "FULL_TIME",
"hire_date": "2024-01-15"
}'


#### Departments

GET /api/v1/organizations/departments/ # List all departments
POST /api/v1/organizations/departments/ # Create department
GET /api/v1/organizations/departments/{id}/ # Get department details
PUT /api/v1/organizations/departments/{id}/ # Update department
DELETE /api/v1/organizations/departments/{id}/ # Delete department
GET /api/v1/organizations/departments/{id}/employees/ # Get dept employees
GET /api/v1/organizations/departments/{id}/hierarchy/ # Get dept hierarchy tree


#### Health Checks

GET /health/ # Service health status
GET /health/ready/ # Readiness probe (all deps ready)
GET /health/live/ # Liveness probe


**Example Response**:

{
"status": "healthy",
"service": "hr-core",
"version": "1.0.0"
}


### GraphQL API

**Endpoint**: `http://localhost:8001/graphql/`

**Schema Documentation**: Available in GraphiQL interface

#### Sample Queries

**Get All Organizations with Employees**
{
allOrganizations {
id
name
email
employeeCount
departmentCount
departments {
id
name
code
employeeCount
}
}
}


**Get All Employees**
{
allEmployees(employment_status: "ACTIVE") {
id
employeeId
fullName
email
phone
jobTitle
organizationName
departmentName
managerName
hireDate
}
}


**Search Employees**
{
searchEmployees(query: "john") {
id
fullName
email
jobTitle
}
}


**Get Organization with Complete Hierarchy**

{
organization(id: 1) {
id
name
employeeCount
departments {
id
name
employeeCount
employees {
id
fullName
jobTitle
}
}
}
}


---

## 🐳 Services

### Service Overview

| Service | Port(s) | Purpose | Status |
|---------|---------|---------|--------|
| **hr-core** | 8001 | Django API | ✅ Running |
| **postgres** | 5432 | Primary database | ✅ Running |
| **redis** | 6379 | Cache & sessions | ✅ Running |
| **mongodb** | 27017 | Audit logs | ✅ Running |
| **neo4j** | 7474, 7687 | Org hierarchy | ✅ Running |
| **keycloak** | 8180 | Authentication | ✅ Running |
| **minio** | 9000, 9001 | Object storage | ✅ Running |
| **traefik** | 80, 8080 | API Gateway | ✅ Running |

### Service Details

#### hr-core (Django)
- **Technology**: Django 5.0.7, DRF, Graphene
- **Port**: 8001
- **Health Check**: http://localhost:8001/health/
- **Admin Panel**: http://localhost:8001/admin/
- **GraphQL**: http://localhost:8001/graphql/

#### PostgreSQL
- **Version**: 15-alpine
- **Port**: 5432
- **Databases**: 
  - `keycloak` - Keycloak data
  - `hr_core_db` - HR application data
  - `payroll_db` - Payroll data (future)
  - `postgres` - Default database
- **Credentials**: 
  - User: `hr_admin`
  - Password: `hr_secure_password_2025`

#### MongoDB
- **Version**: 7
- **Port**: 27017
- **Database**: `hr_lookout_audit`
- **Collection**: `audit_logs`
- **Credentials**:
  - User: `mongo_admin`
  - Password: `mongo_secure_password_2025`

#### Neo4j
- **Version**: 5-community
- **Ports**: 7474 (HTTP), 7687 (Bolt)
- **Browser**: http://localhost:7474
- **Database**: `hr_lookout_graph`
- **Purpose**: Organizational hierarchy relationships
- **Credentials**:
  - User: `neo4j`
  - Password: `neo4j_secure_password_2025`

#### Redis
- **Version**: 7-alpine
- **Port**: 6379
- **Purpose**: Caching, session storage
- **Credentials**:
  - Password: `redis_secure_password_2025`

#### Keycloak
- **Version**: 23.0
- **Port**: 8180
- **Admin Console**: http://localhost:8180
- **Realm**: `hr-lookout`
- **Credentials**:
  - User: `admin`
  - Password: `admin123`

#### MinIO
- **Version**: latest
- **Ports**: 9000 (API), 9001 (Console)
- **Console**: http://localhost:9001
- **Bucket**: `hr-documents`
- **Credentials**:
  - Access Key: `minio_admin`
  - Secret Key: `minio_secure_password_2025`

#### Traefik
- **Version**: 2.10
- **Ports**: 80 (HTTP), 8080 (Dashboard)
- **Dashboard**: http://localhost:8080
- **Purpose**: API Gateway, reverse proxy, load balancer

---

## 💻 Development

### Daily Workflow

**Start Development**

Start all services
docker-compose up -d

Check status
docker-compose ps

View logs
docker-compose logs -f hr-core


**Making Code Changes**
- Edit files in `services/hr-core/`
- Django auto-reloads (no restart needed)
- For dependency changes: rebuild with `docker-compose build hr-core`

**Database Migrations**

Create migrations
docker-compose exec hr-core python manage.py makemigrations

Apply migrations
docker-compose exec hr-core python manage.py migrate

View migration status
docker-compose exec hr-core python manage.py showmigrations


**Django Shell**
Access Django shell
docker-compose exec hr-core python manage.py shell

Example operations:
from hr_core.apps.employees.models import Employee
employees = Employee.objects.all()


**Database Access**
PostgreSQL
docker-compose exec postgres psql -U hr_admin -d hr_core_db

MongoDB
docker-compose exec mongodb mongosh -u mongo_admin -p mongo_secure_password_2025

Redis
docker-compose exec redis redis-cli


### Environment Variables

Located in `.env` file:

PostgreSQL
POSTGRES_USER=hr_admin
POSTGRES_PASSWORD=hr_secure_password_2025
POSTGRES_DB=postgres

Redis
REDIS_PASSWORD=redis_secure_password_2025

MongoDB
MONGO_INITDB_ROOT_USERNAME=mongo_admin
MONGO_INITDB_ROOT_PASSWORD=mongo_secure_password_2025

Neo4j
NEO4J_AUTH=neo4j/neo4j_secure_password_2025

Keycloak
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=admin123

MinIO
MINIO_ROOT_USER=minio_admin
MINIO_ROOT_PASSWORD=minio_secure_password_2025

### Testing

**Run Django Tests**
docker-compose exec hr-core python manage.py test

**Manual API Testing**
Health check
curl http://localhost:8001/health/

List organizations
curl http://localhost:8001/api/v1/organizations/

List employees
curl http://localhost:8001/api/v1/employees/

---

## 🐛 Troubleshooting

### Common Issues

**Services Won't Start**
Check logs for errors
docker-compose logs

Restart all services
docker-compose restart

Clean restart (removes containers)
docker-compose down
docker-compose up -d

**Database Connection Errors**
Verify databases are healthy
docker-compose ps

Check hr-core logs
docker-compose logs hr-core

Manually run migrations
docker-compose exec hr-core python manage.py migrate

**Port Already in Use**
Find process using port (example: 8001)
netstat -ano | findstr :8001

Stop the process
taskkill /PID <process_id> /F

Or change port in docker-compose.yml

**Permission Errors (403)**
- Authentication is disabled for development
- Check that `permission_classes` are commented out in views
- Verify REST_FRAMEWORK settings have `AllowAny`

**GraphQL Errors**
- Ensure Keycloak middleware is disabled
- Check Django logs: `docker-compose logs hr-core`
- Verify all apps are in INSTALLED_APPS

**Docker Build Failures**
Clean build
docker-compose build hr-core --no-cache

If DNS issues persist
Configure Docker Desktop → Docker Engine → Add:
{
"dns": ["8.8.8.8", "8.8.4.4"]
}

---

## 📁 Project Structure

HR-Lookout/
├── docker-compose.yml # Service orchestration
├── .env # Environment variables
├── .gitignore # Git ignore rules
├── README.md # This file
│
├── init-scripts/ # Database initialization
│ └── init-db.sql # PostgreSQL init script
│
├── services/
│ └── hr-core/ # Django microservice
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── requirements.txt
│ ├── manage.py
│ │
│ ├── config/ # Django project settings
│ │ ├── init.py
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── wsgi.py
│ │ ├── asgi.py
│ │ └── schema.py # GraphQL schema
│ │
│ ├── hr_core/
│ │ └── apps/
│ │ ├── authentication/ # Keycloak integration
│ │ │ ├── backends.py
│ │ │ ├── middleware.py
│ │ │ ├── exceptions.py
│ │ │ └── views.py
│ │ │
│ │ ├── audit/ # Audit logging
│ │ │ ├── logger.py
│ │ │ └── middleware.py
│ │ │
│ │ ├── employees/ # Employee management
│ │ │ ├── models.py
│ │ │ ├── serializers.py
│ │ │ ├── views.py
│ │ │ ├── urls.py
│ │ │ ├── admin.py
│ │ │ └── migrations/
│ │ │
│ │ └── organizations/ # Org management
│ │ ├── models.py
│ │ ├── serializers.py
│ │ ├── views.py
│ │ ├── urls.py
│ │ ├── admin.py
│ │ ├── neo4j_service.py
│ │ └── migrations/
│ │
│ ├── staticfiles/ # Collected static files
│ └── scripts/
│ ├── migrate.sh
│ └── migrate.ps1
│
└── data/ # Persistent data (gitignored)
├── postgres/
├── mongodb/
├── neo4j/
├── redis/
└── minio/

---

## 🗺️ Roadmap

### ✅ Phase 0: Planning (Complete)
- Requirements analysis
- Architecture design
- Technology stack selection

### ✅ Phase 1: Infrastructure (Complete)
- Docker Compose setup
- PostgreSQL, MongoDB, Neo4j, Redis
- Keycloak authentication server
- MinIO object storage
- Traefik API gateway

### ✅ Phase 2: Backend MVP (Complete)
- Django project structure
- Employee & Organization models
- REST APIs with Django REST Framework
- GraphQL APIs with Graphene-Django
- Database migrations
- Health check endpoints
- Django Admin panel
- Audit logging framework

### ⏳ Phase 3: Web Frontend (Planned)
- Next.js 14 with TypeScript
- Tailwind CSS styling
- Employee management UI
- Organization hierarchy viewer
- Department management
- Dashboard with analytics
- Keycloak authentication integration

### ⏳ Phase 4: Mobile App (Planned)
- React Native with Expo
- Employee directory
- Profile management
- Organization chart
- Document viewer
- Push notifications

### ⏳ Phase 5: Additional Services (Planned)
- Payroll microservice (Node.js/NestJS)
- Reports microservice (Python/FastAPI)
- Notifications service (WebSockets)
- Analytics service

---

## 📊 Database Schema

### PostgreSQL Tables

**organizations**
- Organization master data
- Tax and legal information
- Contact details

**departments**
- Department structure
- Hierarchy relationships
- Cost center tracking

**employees**
- Employee records
- Personal information
- Employment details
- Reporting relationships

**employee_documents**
- Document metadata
- File references (MinIO)
- Upload tracking

### MongoDB Collections

**audit_logs**
- All API operations
- User actions
- IP addresses & timestamps
- Before/after values

### Neo4j Graph

**Employee Nodes**
- REPORTS_TO relationships
- Organizational hierarchy
- Team structures

---

## 📝 Development Notes

### Current Configuration (Development Mode)

⚠️ **NOT FOR PRODUCTION**

- Authentication disabled
- AllowAny permissions
- Default passwords
- DEBUG mode enabled
- No HTTPS

### Authentication Framework (Disabled)

Keycloak integration is implemented but disabled for development:

config/settings.py - Currently commented out:
MIDDLEWARE = [
'hr_core.apps.authentication.middleware.KeycloakAuthenticationMiddleware',
]
REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': [
'hr_core.apps.authentication.backends.KeycloakAuthentication',
],
}

### Known Issues

1. **Keycloak Authentication**: Disabled due to `python-keycloak` library incompatibility
2. **Neo4j Sync**: Employee-to-Neo4j sync not yet triggered automatically
3. **Department Head**: Field exists but circular dependency handled via two-stage migration

---

## 🔐 Security

### Development Credentials

All default passwords should be changed for production:

| Service | Username | Password |
|---------|----------|----------|
| Django Admin | admin | (set during createsuperuser) |
| PostgreSQL | hr_admin | hr_secure_password_2025 |
| MongoDB | mongo_admin | mongo_secure_password_2025 |
| Redis | - | redis_secure_password_2025 |
| Neo4j | neo4j | neo4j_secure_password_2025 |
| Keycloak | admin | admin123 |
| MinIO | minio_admin | minio_secure_password_2025 |

### Production Checklist (TODO)

- [ ] Enable Keycloak authentication
- [ ] Set strong passwords
- [ ] Disable DEBUG mode
- [ ] Configure HTTPS/SSL
- [ ] Set up CORS properly
- [ ] Implement rate limiting
- [ ] Enable audit logging
- [ ] Set up monitoring
- [ ] Configure backups

---

## 📞 Support

### Getting Help

- **Issues**: Check logs with `docker-compose logs -f hr-core`
- **Documentation**: See API docs at `/graphql/` or REST endpoints
- **Database**: Access Django shell for ORM operations

### Useful Commands

View service status
docker-compose ps

Restart specific service
docker-compose restart hr-core

View logs
docker-compose logs -f hr-core

Execute Django command
docker-compose exec hr-core python manage.py <command>

Access container shell
docker-compose exec hr-core bash

Stop all services
docker-compose down

Clean everything (including volumes)
docker-compose down -v

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

Built with:
- Django & Django REST Framework
- Graphene-Django
- PostgreSQL, MongoDB, Neo4j, Redis
- Keycloak
- MinIO
- Traefik
- Docker & Docker Compose

---

**Last Updated**: October 25, 2025  
**Version**: 1.0.0  
**Status**: Phase 2 Complete ✅
