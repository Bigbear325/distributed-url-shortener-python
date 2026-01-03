# Distributed URL Shortener (Python Version)

A high-performance, distributed URL shortening service built with **Python (FastAPI)** to demonstrate system design concepts for Senior Software Engineer interviews.

## 🚀 Features

- **Distributed ID Generation**: Uses a Redis-based block allocator strategy to ensure unique, non-colliding short codes (Ported to Python `asyncio`).
- **High Performance**:
  - **FastAPI**: Modern, high-performance async web framework.
  - **Redis Cache**: Look-aside cache pattern for sub-millisecond redirects.
  - **SQLAlchemy Async**: Non-blocking database operations.
- **Scalable Architecture**: Stateless backend, horizontally scalable.
- **Premium UI**: Modern React frontend with glassmorphism design.

## 🛠 Tech Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **Database**: PostgreSQL (Async via `asyncpg`)
- **Cache / Counter**: Redis (Async via `redis-py`)
- **Frontend**: React, Vite
- **Infrastructure**: Docker Compose

## 🏃‍♂️ Getting Started

### Prerequisites
- Docker & Docker Compose

### Running Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bigbear325/distributed-url-shortener-python.git
   cd distributed-url-shortener-python
   ```

2. **Start Infrastructure & Backend**
   ```bash
   make db
   ```
   This starts Postgres, Redis, and the FastAPI Backend in Docker containers.

3. **Start Frontend**
   Open a new terminal:
   ```bash
   make frontend
   ```

4. **Visit the App**
   Open http://localhost:5173

## 🧪 API Endpoints

- `POST /api/v1/shorten`
- `GET /:shortCode`

## 📝 License

MIT
