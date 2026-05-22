from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rutas import simulation

app = FastAPI(
    title="Cálculo Vectorial — Superficies Cónicas",
    description="API para clasificar y visualizar superficies cuádricas en 3D.",
    version="2.0.0"
)

# CORS para que el frontend pueda llamar al backend localmente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(simulation.router)

# Archivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return {
        "proyecto": "Cálculo Vectorial — Superficies Cónicas",
        "version": "2.0",
        "endpoints": {
            "clasificar": "POST /conicas/clasificar",
            "docs": "/docs"
        }
    }
