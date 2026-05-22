from pydantic import BaseModel
from typing import Optional

class ConicaInput(BaseModel):
    """
    Ecuación cuadrática general en 3D:
    A·x² + B·y² + C·z² + D·xy + E·xz + F·yz + G·x + H·y + I·z + J = 0
    """
    A: float = 0.0
    B: float = 0.0
    C: float = 0.0
    D: float = 0.0  # xy
    E: float = 0.0  # xz
    F: float = 0.0  # yz
    G: float = 0.0  # x
    H: float = 0.0  # y
    I: float = 0.0  # z
    J: float = 0.0  # constante

    # Punto para evaluar el gradiente
    px: float = 0.0
    py: float = 0.0
    pz: float = 0.0


class GradienteInfo(BaseModel):
    gx: float
    gy: float
    gz: float
    magnitud: float


class ConicaOutput(BaseModel):
    tipo: str
    descripcion: str
    ecuacion_latex: str
    gradiente: GradienteInfo
    valor_en_punto: float
    punto_en_superficie: bool
    puntos_grafica: dict  # datos x, y, z para Plotly
