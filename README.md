# hybrid-recommendation-iitisoc
# Hybrid Infinite Scroll Recommendation System

A hybrid recommendation system built for an infinite-scroll content platform. The system combines multiple recommendation techniques with a machine learning ranking model to deliver personalized recommendations while maintaining low latency through offline precomputation, Redis caching, and backend pagination.

## Tech Stack

- Frontend: React
- Backend: Node.js, Express.js
- Database: PostgreSQL
- Cache: Redis
- Machine Learning: Python, LightGBM, Implicit ALS, Scikit-learn

---

# Project Structure

```
backend/
frontend/
dataset/
experiments/
scripts/
docs/
```

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>
cd hybrid-recommendation-iitisoc
```

---

## 2. Backend Setup

```bash
cd backend
npm install
```

Create a `.env` file inside the `backend` directory:

```env
DB_USER=YOUR_DB_USER
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hybrid_recommendation_db

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 3. PostgreSQL Setup

Create a PostgreSQL database named:

```
hybrid_recommendation_db
```

Execute:

```
scripts/init.sql
```

to create the required tables.

---

## 4. Redis Setup

Install Redis (if not already installed):

```bash
brew install redis
```

Start Redis:

```bash
brew services start redis
```

or

```bash
redis-server
```

Verify:

```bash
redis-cli ping
```

Expected output:

```
PONG
```

---

## 5. Frontend Setup

```bash
cd frontend
npm install
```

---

## 6. Run the Backend

```bash
cd backend
npm run dev
```

---

## 7. Run the Frontend

```bash
cd frontend
npm run dev
```

The application will be available at:

```
http://localhost:5173
```

---

# Notes

- Recommendations are generated offline and stored in the PostgreSQL `recommendations` table.
- The backend serves recommendations through paginated API endpoints.
- Redis caches recommendation batches to further reduce response latency.
- The frontend displays recommendation latency and cache statistics in real time.

---

For detailed information regarding the system architecture, recommendation pipeline, methodology, and implementation details, please refer to the end-eval report.
