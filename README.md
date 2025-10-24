# HR-Lookout

**HR-Lookout** is a full-stack, multi-platform HR management system built with a true microservice architecture. It is designed for infinite scalability and production-grade deployments.

---

## 🏗️ Architecture Overview

### Tech Stack

- **Monorepo**: pnpm workspaces
- **Backend**: Multiple independent Django microservices (Python 3.11+)
- **Frontend (Web)**: Next.js (TypeScript)
- **Mobile**: React Native (Expo)
- **API Gateway**: Traefik
- **Authentication**: Keycloak (SSO, OAuth)
- **Databases**:
  - PostgreSQL (core relational data)
  - Redis (caching, background jobs)
  - MongoDB (audit trails, logs)
  - Neo4j (org chart, relationships)
- **File Storage**: AWS S3 (production), MinIO (local dev)
- **APIs**: REST (DRF) + GraphQL (Graphene-Django)
- **Production Infra**: Kubernetes + Terraform
- **Monitoring**: Prometheus + Grafana
- **Error Tracking**: Sentry

---

## 📂 Project Structure

hr-lookout/
├── services/ # Backend microservices (Django)
│ ├── hr-core/
│ ├── payroll/
│ └── ...
├── platforms/ # Frontend applications
│ ├── web/ # Next.js web app
│ └── mobile/ # React Native (Expo) app
├── packages/ # Shared code (TypeScript, Python)
│ ├── api-client/
│ ├── ui/
│ └── ...
├── infra/ # Infrastructure as Code
│ ├── docker/
│ ├── k8s/
│ ├── terraform/
│ └── ...
├── pnpm-workspace.yaml
├── package.json
├── docker-compose.yml
├── development_log.txt
├── .gitignore
├── .editorconfig
└── README.md


---

## 🚀 Development Phases

The project is built incrementally:

- **Phase 0**: Preparation & Monorepo Init ✅
- **Phase 1**: Core Infrastructure (Docker Compose)
- **Phase 2**: Backend MVP (HRIS Microservice)
- **Phase 3**: Frontend MVP (Web App)
- **Phase 4**: Mobile MVP (Expo App)
- **Phase 5**: Backend (Payroll Microservice)
- **Phase 6**: Testing & QA
- **Phase 7**: CI/CD & Production Infra (Kubernetes)
- **Phase 8**: Observability & Hardening

---

## 📋 Prerequisites

- **Node.js**: v18+
- **pnpm**: v8+
- **Python**: 3.11+
- **Docker & Docker Compose**: Latest
- **Git**: Latest

---

## 🛠️ Getting Started

### Phase 0: Initialization (Complete)

The monorepo structure has been initialized. See `development_log.txt` for detailed changes.

### Next: Phase 1

Run the following to set up the local development environment with Docker Compose:

Coming in Phase 1
docker-compose up

Start all services
docker-compose up -d

View logs
docker-compose logs -f

Stop all services
docker-compose down

Stop and remove volumes (CAUTION: deletes all data)
docker-compose down -v



---

## 📖 Documentation

- [PRD (Product Requirements Document)](./PRD.docx)
- [Development Log](./development_log.txt)

---

## 🤝 Contributing

This project follows a strict, phase-by-phase development model. All contributions must align with the current phase and the overall architecture goals.

---

## 📄 License

MIT License. See [LICENSE](./LICENSE) for details.

---

## 🌟 Vision

HR-Lookout aims to be a Rippling-like, full-suite HRIS platform for SMEs, with infinite scalability, intelligent automation, and global compliance.

---

**Built with ❤️ by the HR-Lookout Team**
