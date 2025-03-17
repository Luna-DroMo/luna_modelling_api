# Luna Modelling API Specification

## Table of Contents

1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [API Design](#api-design)
5. [Database Design](#database-design)
6. [Caching and Rate Limiting](#caching-and-rate-limiting)
7. [Development Setup](#development-setup)
8. [Deployment](#deployment)
9. [Best Practices](#best-practices)

## Overview

Luna Modelling API is a FastAPI-based service that provides Kalman filtering capabilities through a RESTful API interface. The service is designed to process time series data using state-of-the-art filtering techniques while maintaining scalability and performance.

### Key Features

- RESTful API endpoints for Kalman filtering
- Account-based authentication
- Rate limiting and quota management
- Containerized deployment
- Asynchronous processing
- Cache-database synchronization

## Technology Stack

### Core Technologies

- **Python 3.9+**: Main programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **NumPy**: Numerical computing library for Kalman filter implementation
- **Redis**: In-memory data store for caching and rate limiting
- **PostgreSQL**: Primary database
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

### Key Dependencies

- **asyncpg**: Asynchronous PostgreSQL driver
- **alembic**: Database migration tool
- **uvicorn**: ASGI server
- **python-jose**: JWT token handling
- **passlib**: Password hashing

## Project Structure

```
luna_modelling_api/
├── api/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── kalman.py
│   └── deps.py
├── core/
│   ├── config.py
│   └── security.py
├── models/
│   ├── account.py
│   └── base.py
├── modelling/
│   ├── kalman_filter.py
│   └── constants.py
├── alembic/
│   └── versions/
├── tests/
├── docker/
├── .env
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## API Design

### Authentication

- API Key-based authentication
- Keys stored in database with UUID format
- Verification through dependency injection

### Endpoints

#### Kalman Filter Endpoint

```python
POST /api/v1/{account_id}/kalman
```

**Input Schema:**

```python
class KalmanInput(BaseModel):
    results: List[float]
```

**Output Schema:**

```python
class KalmanOutput(BaseModel):
    processed_results: List[float]
    input_data: List[float]
```

### Error Handling

- 404: Resource not found
- 403: Authorization error
- 422: Validation error
- 429: Rate limit exceeded
- 500: Internal server error

## Database Design

### Account Table

```sql
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    account_name VARCHAR(255) UNIQUE NOT NULL,
    api_key UUID UNIQUE NOT NULL,
    quota_limit INTEGER NOT NULL DEFAULT 500,
    quota_used INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### SQLAlchemy Models

```python
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    account_name = Column(String, unique=True, nullable=False)
    api_key = Column(UUID(as_uuid=True), unique=True, nullable=False)
    quota_limit = Column(Integer, nullable=False, default=500)
    quota_used = Column(Integer, nullable=False, default=0)
```

## Caching and Rate Limiting

### Redis Schema

```
Key: user:{user_id}:quota
Value: {remaining_quota}
Expiry: None (Managed through sync process)
```

### Synchronization Patterns

#### Delta-Based Synchronization

1. Update Redis in real-time
2. Track delta changes
3. Periodically sync with database
4. Reset delta counter after sync

#### Event-Driven Synchronization

1. Emit quota change events
2. Process events asynchronously
3. Update both Redis and database
4. Maintain event log for audit

## Development Setup

### Local Development

1. Clone repository
2. Create virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
5. Run migrations:
   ```bash
   alembic upgrade head
   ```
6. Start development server:
   ```bash
   uvicorn main:app --reload
   ```

### Docker Development

```bash
docker-compose up --build
```

## Deployment

### Docker Configuration

**Dockerfile:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**

```yaml
version: "3.8"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:password@db:5432/luna
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=luna

  redis:
    image: redis:6
```

## Best Practices

### API Development

1. Use Pydantic models for request/response validation
2. Implement proper error handling
3. Use dependency injection for common functionality
4. Document API endpoints using OpenAPI/Swagger
5. Implement rate limiting and quotas

### Database

1. Use migrations for schema changes
2. Implement proper indexing
3. Use connection pooling
4. Implement retry mechanisms
5. Regular backups

### Caching

1. Implement proper cache invalidation
2. Use atomic operations
3. Handle cache misses gracefully
4. Regular synchronization with database
5. Monitor cache hit/miss rates

### Security

1. Store API keys securely
2. Implement rate limiting
3. Use HTTPS in production
4. Regular security audits
5. Input validation

### Monitoring

1. Implement logging
2. Monitor API usage
3. Track error rates
4. Monitor system resources
5. Set up alerts

### Testing

1. Unit tests for core functionality
2. Integration tests for API endpoints
3. Load testing for performance
4. Regular security testing
5. Automated CI/CD pipeline

## Future Improvements

1. Implement WebSocket support for real-time updates
2. Add support for batch processing
3. Implement more sophisticated rate limiting
4. Add support for different Kalman filter configurations
5. Implement analytics dashboard
6. Add support for different time series models
7. Implement automatic scaling based on load
8. Add support for data export/import
