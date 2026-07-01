# Enterprise HRMS Core 🏢

An enterprise-grade Human Resources Management System (HRMS) core platform, designed to be highly modular, scalable, and adaptable to various organizational structures. 

Built with a modern tech stack focusing on strict data integrity, hierarchical validation, and high performance.

## 🌟 Key Features
- **Modular Architecture:** Clean Domain-Driven Design (DDD) separating core personnel logic from dynamic services.
- **Hierarchical Engine:** Advanced cascading validation for complex organizational trees (Divisions, Departments, Branches).
- **Smart Data Ingestion:** Fuzzy-matching algorithms for resilient bulk data import and validation from Excel/JSON.
- **Dynamic Workflows:** Flexible state machines for personnel status management.

## 🛠️ Technology Stack
- **Frontend:** React, Vite, TypeScript, TailwindCSS, Lucide Icons.
- **Backend:** Python, Django, Django REST Framework, PostgreSQL.
- **Tooling:** Docker, Ruff, ESLint.

## 🚀 Quick Start Guide

To deploy the system locally for development or testing, follow these steps:

### 1. Environment Setup
Clone the repository and set up your environment variables by copying the template:
```bash
cp .env.example .env
```
Update the `.env` file with your local database credentials and secret keys.

### 2. Database Initialization
Run the standard Django migrations to build the schema:
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Initial Data (Important)
The system's routing and hierarchical logic depend on initial seed data (Dictionaries, Org Charts, Roles). 
*Note: Due to the dynamic nature of the system, default data is not included in the repository to allow each tenant to use their own structure.*

You must place your organization's seed files in `backend/core/fixtures/` and load them:
```bash
python manage.py loaddata org_structure.json
python manage.py loaddata governorates_directorates.json
python manage.py loaddata departments.json
python manage.py loaddata job_titles_complete.json
```
*(If you are a developer, request the local development seed files from your project maintainer).*

### 4. Running the Application

**Start the Backend Server:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

**Start the Frontend Client:**
```bash
cd frontend-new
npm install
npm run dev
```

Visit `http://localhost:5173` to access the application dashboard.

## 🔄 Git Workflow (For Contributors)

To avoid merge conflicts, please follow this standard workflow:
1. Ensure your local `main` branch is up to date: `git pull origin main`
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: your description"`
4. Push your branch and open a Pull Request.

## 📄 License
This project is proprietary and confidential. Unauthorized copying, distribution, or usage is strictly prohibited.
