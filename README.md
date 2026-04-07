# Symplichain Software Engineering Intern Assignment

## 📌 Overview
This repository contains solutions for:

- Shared Gateway Problem (Rate Limiting & Fair Scheduling)
- Mobile App Architecture
- CI/CD Pipeline using GitHub Actions
- Debugging Strategy for Production Outage

---

## 🧠 Key Design Decisions

- Token Bucket Algorithm for strict rate limiting (≤ 3 req/sec)
- Per-customer queue system for fairness
- Celery + Redis for async processing
- React Native for mobile app
- Docker-ready architecture
- GitHub Actions for CI/CD

---

## 🏗️ Architecture Diagrams
Check `/architecture/diagrams`

---

## 🚀 Run Locally

### Backend
cd backend
pip install -r requirements.txt
python manage.py runserver

### Frontend
cd frontend
npm install
npm start

---

## ⚙️ CI/CD
Workflows located in:
infra/github-actions/

---

## 📄 Submission
PDF available at:
architecture/final-pdf/submission.pdf
