from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import textbook_router, rag_router, auth_router
from .api.user_preferences_router import router as user_preferences_router
from .config.settings import settings


def create_app():
    app = FastAPI(
        title="Textbook Generation API",
        description="API for the AI-native textbook with RAG chatbot",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(textbook_router.router, prefix=settings.api_prefix)
    app.include_router(rag_router.router, prefix=settings.api_prefix)
    app.include_router(auth_router.router, prefix=settings.api_prefix)
    app.include_router(user_preferences_router, prefix=settings.api_prefix)

    @app.get("/")
    def read_root():
        return {"message": "Textbook Generation API"}

    @app.get("/health")
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "service": "textbook-generation-api"}

    return app


app = create_app()