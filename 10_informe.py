
def armar_informe(idn, series, verificaciones):
    # Empezamos con una lista de líneas de texto.
    lineas = []

    lineas.append("INFORME DE MEDICIONES")
    lineas.append("====================")

    # Identificamos el instrumento.
    lineas.append("")
    lineas.append("INSTRUMENTO")

    if idn is None:
        lineas.append("No identificado")
    else:
        lineas.append("Fabricante: " + str(idn["fabricante"]))
        lineas.append("Modelo: " + str(idn["modelo"]))
        lineas.append("Serie: " + str(idn["serie"]))
        lineas.append("Versión: " + str(idn["version"]))

    # Agregamos los resultados estadísticos.
    lineas.append("")
    lineas.append("ESTADÍSTICAS")

    for serie in series:
        nombre = serie["nombre"]
        unidad = serie["unidad"]
        datos = serie["resumen"]

        if datos is None:
            lineas.append(nombre + ": sin mediciones")
        else:
            linea = (
                nombre
                + " | n: " + str(datos["n"])
                + " | Promedio: " + format(datos["promedio"], ".2f")
                + " " + unidad
                + " | Mínimo: " + format(datos["minimo"], ".2f")
                + " " + unidad
                + " | Máximo: " + format(datos["maximo"], ".2f")
                + " " + unidad
            )
            lineas.append(linea)

    # Agregamos las verificaciones.
    lineas.append("")
    lineas.append("VERIFICACIONES")

    for verificacion in verificaciones:
        canal = verificacion["canal"]
        coincide = verificacion["coincide"]

        if coincide is True:
            estado = "CORRECTO"
        elif coincide is False:
            estado = "NO COINCIDE"
        else:
            estado = "NO VERIFICADO"

        lineas.append(str(canal) + ": " + estado)

    # Unimos las líneas en una sola cadena.
    informe = "\n".join(lineas)

    return informe


# Pruebas obligatorias.
if __name__ == "__main__":

    # Datos de ejemplo para probar sin conectar el instrumento.
    instrumento = {
        "fabricante": "OWON",
        "modelo": "ADS3202",
        "serie": "12345",
        "version": "1.0"
    }

    series = [
        {
            "nombre": "CH1 - Frecuencia",
            "unidad": "Hz",
            "resumen": {
                "n": 3,
                "minimo": 998.0,
                "maximo": 1002.0,
                "promedio": 1000.0,
                "desvio": 2.0
            }
        }
    ]

    verificaciones = [
        {"canal": "CH1", "coincide": True},
        {"canal": "CH2", "coincide": False}
    ]

    informe = armar_informe(instrumento, series, verificaciones)

    # Prueba 1: identifica el instrumento.
    assert "ADS3202" in informe

    # Prueba 2: incluye las estadísticas.
    assert "1000.00 Hz" in informe

    # Prueba 3: incluye el resultado de las verificaciones.
    assert "CH1: CORRECTO" in informe
    assert "CH2: NO COINCIDE" in informe

    # Prueba 4: instrumento no identificado.
    sin_id = armar_informe(None, [], [])
    assert "No identificado" in sin_id

    print("Todas las pruebas del módulo 10 pasaron.")
    print()
    print(informe)
