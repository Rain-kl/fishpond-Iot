# api/__init__.py

from fastapi import FastAPI

from .router import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="KB Service API",
        description="API for monitoring and controlling the crawling service",
        version="1.0.0"
    )

    # Include the API router
    app.include_router(router, prefix="/api")

    return app


app = create_app()
