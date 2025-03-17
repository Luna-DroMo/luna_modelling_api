from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.routes import health, kalman


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan
)

# Set CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(kalman.router, prefix=settings.API_V1_PREFIX)
