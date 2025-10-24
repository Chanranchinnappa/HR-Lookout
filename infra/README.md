# Infrastructure Documentation

This directory contains all infrastructure-related configuration for the HR-Lookout project.

## Directory Structure

infra/
├── docker/ # Docker Compose and container configs
│ ├── traefik/ # Traefik API Gateway configuration
│ ├── keycloak/ # Keycloak realm and configuration
│ ├── postgres/ # PostgreSQL initialization scripts
│ ├── mongodb/ # MongoDB initialization scripts
│ ├── redis/ # Redis configuration (if needed)
│ ├── neo4j/ # Neo4j configuration (if needed)
│ └── minio/ # MinIO configuration (if needed)
├── k8s/ # Kubernetes manifests (Phase 7)
├── terraform/ # Terraform IaC scripts (Phase 7)
└── README.md

Start all services
docker-compose up -d

View logs
docker-compose logs -f

Stop all services
docker-compose down

Stop and remove volumes (CAUTION: deletes all data)
docker-compose down -v


### Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Traefik Dashboard | http://localhost:8080 | N/A |
| Keycloak Admin | http://localhost:8180 | admin / keycloak_admin_password_2025 |
| Keycloak (via Traefik) | http://auth.localhost | admin / keycloak_admin_password_2025 |
| PostgreSQL | localhost:5432 | hr_admin / hr_secure_password_2025 |
| Redis | localhost:6379 | redis_secure_password_2025 |
| MongoDB | localhost:27017 | mongo_admin / mongo_secure_password_2025 |
| Neo4j Browser | http://localhost:7474 | neo4j / neo4j_secure_password_2025 |
| MinIO Console | http://localhost:9001 | minio_admin / minio_secure_password_2025 |
| MinIO API | http://localhost:9000 | minio_admin / minio_secure_password_2025 |

### Keycloak Test Users

Three test users are pre-configured in the `hr-lookout` realm:

1. **Admin User**
   - Username: `admin`
   - Password: `admin123`
   - Roles: `hr_admin`

2. **Manager User**
   - Username: `hr.manager`
   - Password: `manager123`
   - Roles: `hr_manager`, `employee`

3. **Employee User**
   - Username: `employee`
   - Password: `employee123`
   - Roles: `employee`

### MinIO Buckets

Three buckets are automatically created:

- `hr-documents` - For general document storage
- `hr-profile-pictures` - For employee profile pictures (public read)
- `hr-reports` - For generated reports

### Database Configuration

#### PostgreSQL Databases

- `hr_lookout` (default) - Shared database
- `keycloak` - Keycloak authentication data
- `hr_core_db` - HR Core microservice data (Phase 2)
- `payroll_db` - Payroll microservice data (Phase 5)

#### MongoDB Databases

- `hr_lookout_audit` - Audit logs, error logs, system events

#### Neo4j

- Configured with APOC and Graph Data Science plugins
- Used for org chart and employee relationships (Phase 2+)

### Troubleshooting

#### Keycloak not starting

- Ensure PostgreSQL is healthy first: `docker-compose logs postgres`
- Check Keycloak logs: `docker-compose logs keycloak`
- Keycloak takes 30-60 seconds to start initially

#### MinIO buckets not created

- Check minio-init logs: `docker-compose logs minio-init`
- Manually run: `docker-compose up minio-init`

#### Port conflicts

- Edit `.env` file to change default ports
- Common conflicts: 5432 (PostgreSQL), 6379 (Redis), 27017 (MongoDB)

### Health Checks

All services have health checks configured. To verify:


All services should show `healthy` status.

## Production Infrastructure (Phase 7)

Production infrastructure will use:

- **Kubernetes (EKS)** for container orchestration
- **Terraform** for infrastructure provisioning
- **Helm** for application deployment
- **AWS RDS** for PostgreSQL (managed)
- **AWS ElastiCache** for Redis (managed)
- **AWS DocumentDB** for MongoDB-compatible storage
- **AWS S3** for object storage
- **External Keycloak** or **AWS Cognito** for authentication

---

**Note**: This is a local development setup. Do not use these credentials or configurations in production.
