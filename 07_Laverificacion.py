
# ============================================================

# EJERCICIO 7: LA VERIFICACION
# ============================================================

import math
from importlib import import_module

a_numero = import_module("02_magnitudes").a_numero
con_unidad = import_module("02_magnitudes").con_unidad


# ============================================================
# FUNCION 1: CALCULO DEL VRMS TEORICO
# ============================================================

def vrms_teorico(vpp):

    # Verifica que Vpp sea un numero valido.
    if isinstance(vpp, bool) or not isinstance(vpp, (int, float)):
        return None

    # Rechaza valores infinitos, NaN o negativos.
    if not math.isfinite(vpp) or vpp < 0:
        return None

    # Calcula el valor eficaz de una señal senoidal.
    vrms = vpp / (2 * math.sqrt(2))

    return vrms


# ============================================================
# FUNCION 2: VERIFICACION DE TOLERANCIA
# ============================================================

def coincide(medido, teorico, tolerancia=0.02):

    # Verifica que los tres parametros sean numeros validos.
    for valor in (medido, teorico, tolerancia):

        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            return False

        if not math.isfinite(valor):
            return False

    # Rechaza valores negativos.
    if medido < 0 or teorico < 0 or tolerancia < 0:
        return False

    # Evita dividir por cero.
    if teorico == 0:
        return medido == 0

    # Calcula el error relativo.
    error_relativo = abs(medido - teorico) / abs(teorico)

    # Comprueba si el error esta dentro de la tolerancia.
    return error_relativo <= tolerancia


# ============================================================
# FUNCION 3: VERIFICACION DE UN CANAL
# ============================================================

def verificar_canal(filas, canal):

    # Inicializa los valores de medicion.
    vpp = None
    vrms_medido = None

    # Recorre las mediciones del ejercicio 6.
    for fila in filas:

        # Ignora las mediciones de otros canales.
        if fila["canal"] != canal:
            continue

        # Obtiene la tension pico a pico.
        if fila["magnitud"] == "PKPK":
            vpp = fila["valor"]

        # Obtiene el valor eficaz medido.
        elif fila["magnitud"] == "CYCRMS":
            vrms_medido = fila["valor"]

    # Calcula el Vrms teorico.
    vrms_esperado = vrms_teorico(vpp)

    # Compara los valores medido y teorico.
    resultado = coincide(vrms_medido, vrms_esperado)

    # Devuelve los resultados en un diccionario.
    return {
        "canal": canal,
        "vpp": vpp,
        "vrms_medido": vrms_medido,
        "vrms_teorico": vrms_esperado,
        "coincide": resultado
    }


# ============================================================
# PRUEBAS DEL EJERCICIO 7
# ============================================================

if __name__ == "__main__":

    # Mediciones simuladas con el formato del ejercicio 6.
    filas = [
        {"canal": "CH1", "magnitud": "FREQ", "valor": 1000.0},
        {"canal": "CH1", "magnitud": "PKPK", "valor": 2.0},
        {"canal": "CH1", "magnitud": "CYCRMS", "valor": 0.7071},
        {"canal": "CH2", "magnitud": "FREQ", "valor": 2500.0},
        {"canal": "CH2", "magnitud": "PKPK", "valor": 0.8},
        {"canal": "CH2", "magnitud": "CYCRMS", "valor": 0.2828}
    ]


    # PRUEBA 1: CALCULO DEL VRMS TEORICO
    # --------------------------------------------------------

    valor = vrms_teorico(2.0)

    # Compara los valores permitiendo una diferencia minima.
    assert math.isclose(valor, 0.70710678, rel_tol=0.000001)

    print("Prueba 1 OK: Calculo del Vrms teorico")


    # PRUEBA 2: TOLERANCIA DEL 2%
    # --------------------------------------------------------

    assert coincide(0.7071, vrms_teorico(2.0)) is True
    assert coincide(0.750, vrms_teorico(2.0)) is False

    print("Prueba 2 OK: Tolerancia relativa verificada")


    # PRUEBA 3: VERIFICACION DE DOS CANALES
    # --------------------------------------------------------

    resultado_ch1 = verificar_canal(filas, "CH1")
    resultado_ch2 = verificar_canal(filas, "CH2")

    assert resultado_ch1["coincide"] is True
    assert resultado_ch2["coincide"] is True

    print("Prueba 3 OK: CH1 y CH2 coinciden con la teoria")


    # PRUEBA 4: SEÑAL CUADRADA - CASO CRITICO
    # --------------------------------------------------------

    # Una señal cuadrada de 2 Vpp tiene 1 Vrms.
    # No debe coincidir con el valor teorico senoidal.
    filas_cuadrada = [
        {"canal": "CH1", "magnitud": "PKPK", "valor": 2.0},
        {"canal": "CH1", "magnitud": "CYCRMS", "valor": 1.0}
    ]

    resultado_cuadrada = verificar_canal(filas_cuadrada, "CH1")

    assert resultado_cuadrada["coincide"] is False

    print("Prueba 4 OK: Señal cuadrada no coincide")


    # PRUEBA 5: DATOS INVALIDOS
    # --------------------------------------------------------

    assert vrms_teorico(-2.0) is None
    assert vrms_teorico("dos") is None
    assert vrms_teorico(float("nan")) is None

    print("Prueba 5 OK: Datos invalidos rechazados")


    # PRUEBA 6: MEDICION INCOMPLETA
    # --------------------------------------------------------

    filas_incompletas = [
        {"canal": "CH1", "magnitud": "PKPK", "valor": 2.0}
    ]

    resultado_incompleto = verificar_canal(
        filas_incompletas, "CH1"
    )

    assert resultado_incompleto["coincide"] is False
    assert resultado_incompleto["vrms_medido"] is None

    print("Prueba 6 OK: Medicion faltante detectada")


    # PRUEBA 7: VALOR TEORICO IGUAL A CERO
    # --------------------------------------------------------

    assert coincide(0.0, 0.0) is True
    assert coincide(0.1, 0.0) is False

    print("Prueba 7 OK: Caso limite de valor cero")


    # ========================================================
    # PRESENTACION DE RESULTADOS
    # ========================================================

    print("\n========== VERIFICACION DE CANALES ==========\n")

    # Muestra los resultados de ambos canales.
    for resultado in [resultado_ch1, resultado_ch2]:

        print(f"Canal: {resultado['canal']}")

        print(
            "Tension pico a pico:",
            con_unidad(resultado["vpp"], "V")
        )

        print(
            "Vrms medido:",
            con_unidad(resultado["vrms_medido"], "V")
        )

        print(
            "Vrms teorico:",
            con_unidad(resultado["vrms_teorico"], "V")
        )

        # Informa si la medicion cumple la tolerancia.
        if resultado["coincide"]:
            print("Resultado: COINCIDE")
        else:
            print("Resultado: NO COINCIDE")

        print("----------------------------------------")
