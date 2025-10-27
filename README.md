# HR-Lookout

**Modern Microservice-Based Human Resources Information System (HRIS)**

A comprehensive, scalable HRIS platform built with Django REST Framework, Next.js, and modern cloud-native technologies.

---

## 🚀 **Project Overview**

HR-Lookout is an enterprise-grade HRIS designed to streamline HR operations, employee management, and organizational workflows. Built with a microservices architecture, it provides flexibility, scalability, and maintainability for organizations of all sizes.

**Status:** Phase 4 Complete ✅ | In Active Development

---

## ✨ **Features**

### **Current (Phase 4)**
- ✅ **Organization Management** - Complete CRUD with card grid layout
- ✅ **Employee Management** - Full CRUD, search, filtering, table view
- ✅ **Department Management** - Complete CRUD with organizational hierarchy
- ✅ **Real-time Search** - Client-side filtering across all modules
- ✅ **REST API** - Comprehensive RESTful endpoints
- ✅ **GraphQL API** - Flexible query interface with nested relationships
- ✅ **Responsive UI** - Mobile, tablet, and desktop support
- ✅ **Dark Theme** - Modern, accessible interface

### **Infrastructure**
- ✅ **Docker Compose** - Complete containerized development environment
- ✅ **PostgreSQL** - Primary relational database
- ✅ **MongoDB** - Audit logging and analytics
- ✅ **Redis** - Caching layer (configured, not yet utilized)
- ✅ **Neo4j** - Graph database for org charts (configured, sync pending)
- ✅ **Keycloak** - Authentication server (configured, integration pending)
- ✅ **MinIO** - Object storage for documents and media
- ✅ **Traefik** - API gateway and reverse proxy

---

## 🏗️ **Architecture**

### **Monorepo Structure**

HR-Lookout/
├── services/
│   └── hr-core/          # Django REST backend
├── platforms/
│   └── web/              # Next.js frontend  
├── packages/ # Shared libraries
└── infra/
└── docker/ # Docker configurations

### **Technology Stack**

**Backend:**
- Django 5.0.7 + Django REST Framework
- Python 3.11
- PostgreSQL 15 (primary database)
- MongoDB 7 (audit logs)
- Neo4j 5 (org charts)
- Redis 7 (caching)
- Graphene-Django (GraphQL)

**Frontend:**
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- Axios (HTTP client)
- React Icons

**Infrastructure:**
- Docker + Docker Compose
- Traefik (API Gateway)
- Keycloak (Authentication)
- MinIO (Object Storage)

---

## 📋 **Prerequisites**

- **Docker Desktop** (20.10+)
- **Node.js** (18+) and npm/pnpm
- **Python** (3.11+)
- **Git**
- **PowerShell** (Windows) or Bash (Linux/Mac)

---

## 🚀 **Quick Start**

### **1. Clone the Repository**

git clone https://github.com/yourusername/HR-Lookout.git
cd HR-Lookout


### **2. Environment Setup**

Copy environment template
cp .env.example .env

Update .env with your configuration
Default values work for local development


### **3. Start Infrastructure**

Start all services (Postgres, MongoDB, Redis, Neo4j, Keycloak, MinIO)
docker-compose up -d

Check service status
docker-compose ps

View logs
docker-compose logs -f hr-core


### **4. Start Backend (hr-core)**

**Option A: Using Docker (Recommended)**
Backend already running from docker-compose up
Access at http://localhost:8001


**Option B: Local Development**

cd services/hr-core

Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1 # Windows
source venv/bin/activate # Linux/Mac

Install dependencies
pip install -r requirements.txt

Run migrations
python manage.py migrate

Create superuser
python manage.py createsuperuser

Run development server
python manage.py runserver 0.0.0.0:8001


### **5. Start Frontend (web)**

cd services/web

Install dependencies
npm install

Start development server
npm run dev

Access at http://localhost:3000


---

## 🌐 **Access URLs**

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | - |
| **Backend API** | http://localhost:8001/api/v1/ | - |
| **GraphQL Playground** | http://localhost:8001/graphql/ | - |
| **Django Admin** | http://localhost:8001/admin/ | Create superuser |
| **Traefik Dashboard** | http://localhost:8080 | - |
| **Keycloak** | http://localhost:8082 | admin / admin |
| **MinIO Console** | http://localhost:9001 | minioadmin / minioadmin |

---

## 📚 **API Documentation**

### **REST API Endpoints**

**Organizations:**
GET /api/v1/organizations/
POST /api/v1/organizations/
GET /api/v1/organizations/{id}/
PUT /api/v1/organizations/{id}/
DELETE /api/v1/organizations/{id}/

**Employees:**
GET /api/v1/employees/
POST /api/v1/employees/
GET /api/v1/employees/{id}/
PUT /api/v1/employees/{id}/
DELETE /api/v1/employees/{id}/
GET /api/v1/employees/search/?q={query}

**Departments:**
GET /api/v1/departments/
POST /api/v1/departments/
GET /api/v1/departments/{id}/
PUT /api/v1/departments/{id}/
DELETE /api/v1/departments/{id}/

### **GraphQL Queries**
query {
allOrganizations {
id
name
employeeCount
departments {
name
code
}
}

allEmployees(employmentStatus: "ACTIVE") {
id
firstName
lastName
email
jobTitle
organization {
name
}
}
}
---

## 🧪 **Testing**

### **Backend Tests**
cd services/hr-core
python manage.py test

### **Frontend Tests**
cd services/web
npm test

### **API Testing**
Using curl
curl http://localhost:8001/api/v1/organizations/

Using httpie
http GET http://localhost:8001/api/v1/employees/

Using Postman
Import collection from /docs/postman/

---

## 🗄️ **Database Management**

### **Migrations**
Create migrations
docker-compose exec hr-core python manage.py makemigrations

Apply migrations
docker-compose exec hr-core python manage.py migrate

View migration status
docker-compose exec hr-core python manage.py showmigrations

### **Database Shell**
Django shell
docker-compose exec hr-core python manage.py shell

PostgreSQL shell
docker-compose exec postgres psql -U hr_user -d hr_core_db

MongoDB shell
docker-compose exec mongodb mongosh hr_lookout_audit

Neo4j Cypher shell
docker-compose exec neo4j cypher-shell -u neo4j -p hr_lookout_neo4j

---

## 🔧 **Development**

### **Project Structure**

**Backend (services/hr-core):**
hr-core/
├── config/ # Django settings
├── hr_core/
│ └── apps/
│ ├── authentication/ # Keycloak integration
│ ├── audit/ # MongoDB audit logging
│ ├── core/ # Shared models/mixins
│ ├── employees/ # Employee management
│ └── organizations/ # Organization management
└── requirements.txt

**Frontend (services/web):**
web/
├── app/
│ ├── page.tsx # Dashboard
│ ├── employees/ # Employee CRUD
│ ├── organizations/ # Organization CRUD
│ └── departments/ # Department CRUD
├── lib/
│ └── api.ts # API client
├── types/
│ └── index.ts # TypeScript interfaces
└── package.json

### **Code Style**

**Backend:**
- Follow PEP 8
- Use Black for formatting
- Type hints encouraged

**Frontend:**
- ESLint + Prettier
- TypeScript strict mode
- Functional components with hooks

---

## 📦 **Dependencies**

### **Backend (Python)**
Django==5.0.7
djangorestframework==3.14.0
django-cors-headers==4.3.0
psycopg2-binary==2.9.9
pymongo==4.6.0
redis==5.0.1
neo4j==5.14.0
graphene-django==3.1.5

### **Frontend (Node.js)**
{
"dependencies": {
"next": "16.0.0",
"react": "^19.0.0",
"axios": "^1.6.0",
"react-icons": "^5.3.0",
"tailwindcss": "^3.4.1"
}
}

---

## 🚧 **Roadmap**

### **Phase 5: Authentication & Authorization** (Next)
- [ ] Keycloak integration
- [ ] JWT token management
- [ ] Role-based access control
- [ ] Protected routes

### **Future Phases**
- [ ] Document management (MinIO integration)
- [ ] Employee self-service portal
- [ ] Payroll microservice
- [ ] Attendance tracking
- [ ] Performance management
- [ ] Mobile app (React Native)
- [ ] Analytics dashboard
- [ ] Reporting engine

---

## 📖 **Documentation**

- [Development Log](development_log.txt) - Detailed session logs
- [Infrastructure Guide](infra/README.md) - Docker setup and services
- [API Documentation](docs/api/) - Coming soon
- [Contributing Guide](CONTRIBUTING.md) - Coming soon

---

## 🤝 **Contributing**

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting PRs.

### **Development Workflow**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

**Charan Chinnappa P M**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 **Acknowledgments**

- Django Software Foundation
- Next.js by Vercel
- All open-source contributors

---

## 📊 **Project Status**

**Current Version:** v0.4.0  
**Status:** 🟢 Active Development  
**Phase:** 4 of 5 Complete  
**Last Updated:** October 28, 2025

### **Completed Phases:**
- ✅ Phase 0: Monorepo Setup
- ✅ Phase 1: Infrastructure (Docker)
- ✅ Phase 2: Backend MVP (Django)
- ✅ Phase 3: Frontend MVP (Next.js)
- ✅ Phase 4: Department CRUD + Refactoring

### **Statistics:**
- 📦 8 Docker services
- 🔧 3 Database systems
- 🌐 30+ REST API endpoints
- 📊 4 GraphQL queries
- 💻 3 Frontend pages
- 📝 ~5,000 lines of code

---

**Built with ❤️ for modern HR management**
