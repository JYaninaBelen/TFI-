
def resumen(valores):
    # Si la lista esta vacia devuelve None.
    if len(valores) == 0:
        return None

    # Calculamos el numero de elementos, el minimo, el maximo y el promedio.
    n = len(valores)
    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores) / n

    # Sumamos los cuadrados de las diferencias con el promedio.
    suma_cuadrados = 0

    for valor in valores:
        diferencia = valor - promedio
        cuadrado = diferencia ** 2
        suma_cuadrados = suma_cuadrados + cuadrado

    #Si hay un solo dato, el desvio es cero para no generar error.
    if n == 1:
        desvio = 0.0
    else:
        varianza = suma_cuadrados / (n - 1)
        desvio = varianza ** 0.5

    # Devolvemos todos los resultados en un diccionario.
    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "desvio": desvio
    }


def fuera_de_rango(valores, minimo, maximo):
    # Guardamos las posiciones de los valores incorrectos.
    posiciones = []

    for i in range(len(valores)):
        if valores[i] < minimo or valores[i] > maximo:
            posiciones.append(i)

    return posiciones


# Pruebas obligatorias del ejercicio.
if __name__ == "__main__":

    # Prueba 1: lista vacía.
    assert resumen([]) is None

    # Prueba 2: un único valor.
    assert resumen([10])["desvio"] == 0.0

    # Prueba 3: estadística de tres valores.
    datos = resumen([10, 20, 30])
    assert datos["n"] == 3
    assert datos["minimo"] == 10
    assert datos["maximo"] == 30
    assert datos["promedio"] == 20.0
    assert datos["desvio"] == 10.0

    # Prueba 4: valores fuera de rango.
    assert fuera_de_rango([5, 10, 15, 20], 10, 15) == [0, 3]

    # Prueba 5: los extremos del rango están permitidos.
    assert fuera_de_rango([10, 12, 15], 10, 15) == []

    print("Todas las pruebas del módulo 9 pasaron.")
    # Prueba 6: estadísticas con mediciones reales del módulo 8.
    from importlib import import_module

    leer_log = import_module("08_log").leer_log

    grupos, rechazadas = leer_log("mediciones.log")

    frecuencias = []

    for medicion in grupos[("ADS3202", "CH1", "FREQ")]:
        frecuencias.append(medicion["valor"])
    estadisticas = resumen(frecuencias)

    assert abs(estadisticas["promedio"] - 1000) < 5
    assert estadisticas["desvio"] < 5

    print("Prueba con mediciones reales del módulo 9 superada.")
    