"""FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.streaming.infra.controllers.camera_controller import router as camera_router
from src.detection.infra.controllers.detection_controller import router as detection_router

app = FastAPI(
    title="GT-Vision Toten API",
    description="Sistema de Monitoramento de Alunos com Reconhecimento Facial",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(camera_router)
app.include_router(detection_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "GT-Vision Toten API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}
