from fastapi import APIRouter
from schemas import ConicaInput, ConicaOutput
from services.calculations import analizar_conica

router = APIRouter(prefix="/conicas", tags=["Superficies Cónicas"])


@router.post("/clasificar", response_model=ConicaOutput)
def clasificar_superficie(data: ConicaInput):
    """
    Recibe los coeficientes de una ecuación cuadrática general en 3D:
      A·x² + B·y² + C·z² + D·xy + E·xz + F·yz + G·x + H·y + I·z + J = 0

    Retorna:
    - Tipo de superficie (elipsoide, hiperboloide, paraboloide, etc.)
    - Gradiente ∇F en el punto (px, py, pz)
    - Valor F(px, py, pz) para verificar si el punto está en la superficie
    - Puntos 3D para graficar con Plotly
    """
    return analizar_conica(data)
