import numpy as np
from schemas import ConicaInput, ConicaOutput, GradienteInfo


def evaluar_ecuacion(data: ConicaInput, x, y, z):
    """Evalúa F(x,y,z) = Ax²+By²+Cz²+Dxy+Exz+Fyz+Gx+Hy+Iz+J"""
    return (data.A * x**2 + data.B * y**2 + data.C * z**2
            + data.D * x * y + data.E * x * z + data.F * y * z
            + data.G * x + data.H * y + data.I * z + data.J)


def calcular_gradiente(data: ConicaInput, x: float, y: float, z: float) -> GradienteInfo:
    """
    Gradiente de F(x,y,z):
      ∂F/∂x = 2Ax + Dy + Ez + G
      ∂F/∂y = 2By + Dx + Fz + H
      ∂F/∂z = 2Cz + Ex + Fy + I
    """
    gx = 2 * data.A * x + data.D * y + data.E * z + data.G
    gy = 2 * data.B * y + data.D * x + data.F * z + data.H
    gz = 2 * data.C * z + data.E * x + data.F * y + data.I
    magnitud = float(np.sqrt(gx**2 + gy**2 + gz**2))
    return GradienteInfo(gx=round(gx, 6), gy=round(gy, 6), gz=round(gz, 6), magnitud=round(magnitud, 6))


def clasificar_superficie(data: ConicaInput) -> tuple[str, str]:
    """
    Clasifica la superficie usando los coeficientes cuadráticos A, B, C.
    Considera también los términos cruzados D, E, F.
    Retorna (tipo, descripcion).
    """
    A, B, C = data.A, data.B, data.C
    D, E, F = data.D, data.E, data.F
    G, H, I, J = data.G, data.H, data.I, data.J

    # Términos cuadráticos activos
    cuads = [a for a in [A, B, C] if abs(a) > 1e-10]
    tiene_cruzados = any(abs(v) > 1e-10 for v in [D, E, F])
    tiene_lineales = any(abs(v) > 1e-10 for v in [G, H, I])
    n_cuads = len(cuads)

    if n_cuads == 0:
        return ("Plano", "Ecuación lineal en 3D — define un plano en el espacio.")

    signos = [1 if a > 0 else -1 for a in cuads]
    positivos = signos.count(1)
    negativos = signos.count(-1)

    if n_cuads == 3:
        if positivos == 3 or negativos == 3:
            return ("Elipsoide", "Superficie cerrada. Todos los términos cuadráticos tienen el mismo signo. Caso especial: esfera si A=B=C.")
        elif (positivos == 2 and negativos == 1) or (positivos == 1 and negativos == 2):
            return ("Hiperboloide de una hoja" if positivos == 2 else "Hiperboloide de dos hojas",
                    "Superficie abierta generada por la diferencia de cuadrados en tres variables.")
    elif n_cuads == 2:
        if positivos == 2 or negativos == 2:
            if tiene_lineales:
                return ("Paraboloide Elíptico", "Dos términos cuadráticos del mismo signo con un término lineal — forma de cuenco.")
            return ("Cilindro Elíptico", "Dos variables cuadráticas del mismo signo sin la tercera — superficie cilíndrica.")
        else:  # un positivo, un negativo
            if tiene_lineales:
                return ("Paraboloide Hiperbólico", "Superficie en forma de silla de montar (saddle surface). Punto de ensilladura presente.")
            return ("Cilindro Hiperbólico", "Dos variables cuadráticas de signos opuestos — hipérbola extruida.")
    elif n_cuads == 1:
        if tiene_lineales:
            return ("Paraboloide", "Un término cuadrático con términos lineales — paraboloide de revolución.")
        return ("Cilindro Parabólico", "Un solo término cuadrático — parábola extruida en el espacio.")

    if tiene_cruzados:
        return ("Superficie cuádrica rotada", "Términos cruzados presentes — requiere diagonalización para clasificación exacta.")

    return ("Cuádrica General", "Superficie cuadrática en 3D. Analiza los coeficientes para mayor detalle.")


def generar_puntos_grafica(data: ConicaInput) -> dict:
    """
    Genera puntos (x, y, z) para graficar con Plotly.
    Para cada (x, y) resuelve la ecuación cuadrática en z.
    """
    rango = np.linspace(-10, 10, 60)
    X, Y = np.meshgrid(rango, rango)

    A, B, C = data.A, data.B, data.C
    D, E, F = data.D, data.E, data.F
    G, H, I_coef, J = data.G, data.H, data.I, data.J

    if abs(C) > 1e-10 or abs(E) > 1e-10 or abs(F) > 1e-10:
        # Resolver C·z² + (Ex + Fy + I)·z + (Ax² + By² + Dxy + Gx + Hy + J) = 0
        a_coef = C
        b_coef = E * X + F * Y + I_coef
        c_coef = A * X**2 + B * Y**2 + D * X * Y + G * X + H * Y + J

        discriminante = b_coef**2 - 4 * a_coef * c_coef
        mask = discriminante >= 0

        Z1 = np.full_like(X, np.nan)
        Z2 = np.full_like(X, np.nan)
        Z1[mask] = (-b_coef[mask] + np.sqrt(discriminante[mask])) / (2 * a_coef)
        Z2[mask] = (-b_coef[mask] - np.sqrt(discriminante[mask])) / (2 * a_coef)

        # Limitar rango Z para visualización
        Z1 = np.clip(Z1, -15, 15)
        Z2 = np.clip(Z2, -15, 15)

        return {
            "x": X.tolist(),
            "y": Y.tolist(),
            "z1": Z1.tolist(),
            "z2": Z2.tolist(),
            "doble_hoja": True
        }
    elif abs(I_coef) > 1e-10:
        # Resolver linealmente en z: z = -(Ax²+By²+Dxy+Gx+Hy+J) / I
        num = A * X**2 + B * Y**2 + D * X * Y + G * X + H * Y + J
        Z = -num / I_coef
        Z = np.clip(Z, -15, 15)
        return {
            "x": X.tolist(),
            "y": Y.tolist(),
            "z1": Z.tolist(),
            "z2": None,
            "doble_hoja": False
        }
    else:
        # z no aparece — extruir en z
        Z = np.linspace(-10, 10, 60)
        X3, Z3 = np.meshgrid(rango, Z)
        Y3 = np.full_like(X3, np.nan)

        a_coef = B
        if abs(a_coef) > 1e-10:
            b_coef = D * X3 + H
            c_coef = A * X3**2 + G * X3 + J
            disc = b_coef**2 - 4 * a_coef * c_coef
            mask = disc >= 0
            Y3[mask] = (-b_coef[mask] + np.sqrt(disc[mask])) / (2 * a_coef)

        return {
            "x": X3.tolist(),
            "y": Y3.tolist(),
            "z1": Z3.tolist(),
            "z2": None,
            "doble_hoja": False
        }


def construir_latex(data: ConicaInput) -> str:
    """Construye representación LaTeX de la ecuación."""
    terminos = []

    def fmt(coef, var):
        if abs(coef) < 1e-10:
            return None
        c = int(coef) if coef == int(coef) else round(coef, 3)
        if c == 1:
            return var
        elif c == -1:
            return f"-{var}"
        else:
            return f"{c}{var}"

    terminos = list(filter(None, [
        fmt(data.A, "x^2"),
        fmt(data.B, "y^2"),
        fmt(data.C, "z^2"),
        fmt(data.D, "xy"),
        fmt(data.E, "xz"),
        fmt(data.F, "yz"),
        fmt(data.G, "x"),
        fmt(data.H, "y"),
        fmt(data.I, "z"),
    ]))

    if not terminos:
        ec = "0"
    else:
        ec = terminos[0]
        for t in terminos[1:]:
            if t.startswith("-"):
                ec += f" {t}"
            else:
                ec += f" + {t}"

    # Lado derecho: pasamos J al otro lado (rhs = −J)
    j = data.J
    if abs(j) < 1e-10:
        rhs = "0"
    else:
        rhs_val = -j
        rhs = str(int(rhs_val)) if rhs_val == int(rhs_val) else str(round(rhs_val, 4))

    return ec + " = " + rhs


def analizar_conica(data: ConicaInput) -> ConicaOutput:
    tipo, descripcion = clasificar_superficie(data)
    gradiente = calcular_gradiente(data, data.px, data.py, data.pz)
    valor = float(evaluar_ecuacion(data, data.px, data.py, data.pz))
    en_superficie = abs(valor) < 0.5
    puntos = generar_puntos_grafica(data)
    latex = construir_latex(data)

    return ConicaOutput(
        tipo=tipo,
        descripcion=descripcion,
        ecuacion_latex=latex,
        gradiente=gradiente,
        valor_en_punto=round(valor, 6),
        punto_en_superficie=en_superficie,
        puntos_grafica=puntos
    )
