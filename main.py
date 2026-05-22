from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # 1. IMPORTA ESTO
from rutas import simulation

app = FastAPI(
    title="Cálculo Vectorial — Superficies Cónicas",
    description="API para clasificar y visualizar superficies cuádricas en 3D.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation.router)

# Archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. MODIFICA TU RUTA RAÍZ ASÍ:
@app.get("/")
def home():
    # Reemplaza 'index.html' por el nombre real de tu archivo si se llama distinto
    return FileResponse("static/index.html")
