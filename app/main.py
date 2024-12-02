from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.core.logger import logger
from app.core.error_handlers import register_error_handlers
from app.core.database import init_db
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for interacting with PDF documents through chat."
)

# Register routers
app.include_router(upload_router, prefix="/v1", tags=["Upload"])
app.include_router(chat_router, prefix="/v1", tags=["Chat"])

# Register error handlers
register_error_handlers(app)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    await init_db()
    logger.info("Database initialized successfully.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")
