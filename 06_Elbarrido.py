

# Ejercicio 6: El barrido

from importlib import import_module

from importlib import import_module

a_numero = import_module("02_magnitudes").a_numero
con_unidad = import_module("02_magnitudes").con_unidad



def barrer(instrumento, canales):
    """
    Consulta FREQ, PKPK y CYCRMS de cada canal.
    Devuelve una lista de diccionarios con las mediciones.
    """

    magnitudes = [
        ("FREQ", "FREQuency", "Hz"),
        ("PKPK", "PKPK", "V"),
        ("CYCRMS", "CYCRms", "V")
    ]

    mediciones = []

    for canal in canales:
        for magnitud, nombre_scpi, unidad in magnitudes:

            comando = f":MEASUrement:{canal}:{nombre_scpi}?"

            # Consultamos al instrumento
            texto_crudo = instrumento.preguntar(comando)

            # Creamos el registro de medicion
            mediciones.append({
                "canal": canal,
                "magnitud": magnitud,
                "unidad": unidad,
                "crudo": texto_crudo,
                "valor": a_numero(texto_crudo)
            })

    return mediciones


# ----------------------------------------------------------
# INSTRUMENTO SIMULADO PARA LAS PRUEBAS
# ----------------------------------------------------------

class InstrumentoFalso:

    def __init__(self, respuestas=None):
        self.respuestas = respuestas if respuestas is not None else {}
        self.consultas = []

    def preguntar(self, comando):
        self.consultas.append(comando)

        return self.respuestas.get(
            comando, "ERROR: comando desconocido"
        )


# ----------------------------------------------------------
# PRUEBAS DEL EJERCICIO 6
# ----------------------------------------------------------

if __name__ == "__main__":

    respuestas = {
        ":MEASUrement:CH1:FREQuency?": "1.000000E+03",
        ":MEASUrement:CH1:PKPK?": "2.000000E+00",
        ":MEASUrement:CH1:CYCRms?": "7.071000E-01",
        ":MEASUrement:CH2:FREQuency?": "2.500000E+03",
        ":MEASUrement:CH2:PKPK?": "8.000000E-01",
        ":MEASUrement:CH2:CYCRms?": "2.828000E-01"
    }

    # PRUEBA 1: DOS CANALES, SEIS MEDICIONES
    falso = InstrumentoFalso(respuestas)

    filas = barrer(falso, ["CH1", "CH2"])

    assert len(filas) == 6
    assert falso.consultas == list(respuestas)

    print("Prueba 1 OK: Se obtuvieron 6 mediciones en orden")


    # PRUEBA 2: CONVERSION NUMERICA
    assert filas[0] == {
        "canal": "CH1",
        "magnitud": "FREQ",
        "unidad": "Hz",
        "crudo": "1.000000E+03",
        "valor": 1000.0
    }

    assert filas[4]["valor"] == 0.8

    print("Prueba 2 OK: Conversion numerica y texto crudo correctos")


    # PRUEBA 3: CANAL INEXISTENTE
    falso_error = InstrumentoFalso()

    filas_error = barrer(falso_error, ["CH3"])

    assert len(filas_error) == 3

    assert all(
        fila["valor"] is None for fila in filas_error
    )

    assert all(
        fila["crudo"] == "ERROR: comando desconocido"
        for fila in filas_error
    )

    print("Prueba 3 OK: Respuesta de error conservada")


    # PRUEBA 4: RESPUESTA NaN
    falso_nan = InstrumentoFalso({
        ":MEASUrement:CH1:FREQuency?": "NaN"
    })

    filas_nan = barrer(falso_nan, ["CH1"])

    assert filas_nan[0]["valor"] is None
    assert filas_nan[0]["crudo"] == "NaN"

    print("Prueba 4 OK: NaN rechazado sin perder el texto original")


    # PRUEBA 5: LISTA DE CANALES VACIA
    falso_vacio = InstrumentoFalso()

    assert barrer(falso_vacio, []) == []
    assert falso_vacio.consultas == []

    print("Prueba 5 OK: Lista de canales vacia")


    # PRUEBA 6: COMUNICACION CON EL INSTRUMENTO VIRTUAL
    # Importamos la clase Instrumento del ejercicio 5
    Instrumento = import_module("05_cliente").Instrumento

    instrumento = Instrumento()

    try:
        filas_reales = barrer(instrumento, ["CH1", "CH2"])

        assert len(filas_reales) == 6

        assert all(
            fila["valor"] is not None
            for fila in filas_reales
        )

        
        print("\n========== MEDICIONES RECIBIDAS ==========\n")

        for fila in filas_reales:

            print(f"Canal: {fila['canal']}")
            print(f"Magnitud: {fila['magnitud']}")
            print(f"Respuesta original: {fila['crudo']}")

            if fila["valor"] is not None:
                lectura = con_unidad(fila["valor"], fila["unidad"])
                print(f"Medicion: {lectura}")
            else:
                print("Medicion: ERROR - Valor no valido")

            print("----------------------------------------")

        print("Prueba 6 OK: Barrido de 6 mediciones")

    finally:
        instrumento.cerrar()
