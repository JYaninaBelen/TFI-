
# Ejercicio 5 - Cliente TCP para instrumentos virtuales
# Trabajo Final Integrador - UTN FRBA

import socket
import math
from modulo1b import parsear_idn


class Instrumento:

    def __init__(self, ip="127.0.0.1", puerto=5555):
        self.ip = ip
        self.puerto = puerto

        # Creamos el socket TCP
        self.conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print("Intentando conectar...")
            self.conexion.connect((self.ip, self.puerto))
            print("Conexion exitosa")

        except OSError:
            self.conexion.close()
            print("No se pudo conectar con el instrumento")
            raise

        # Almacena los bytes recibidos
        self._buffer = bytearray()

    def enviar(self, comando):
        """Envia un comando SCPI sin esperar respuesta."""

        if not isinstance(comando, str):
            raise TypeError("El comando debe ser texto")

        # Agregamos el salto de linea requerido por el instrumento
        datos = (comando.rstrip("\r\n") + "\n").encode("utf-8")

        # Enviamos los bytes por TCP
        self.conexion.sendall(datos)

    def preguntar(self, comando):
        """Envia una consulta SCPI y devuelve la respuesta."""

        self.enviar(comando)

        # Recibimos hasta encontrar el salto de linea
        while b"\n" not in self._buffer:

            bloque = self.conexion.recv(4096)

            if not bloque:
                raise ConnectionError(
                    "El instrumento cerro la conexion sin responder"
                )

            self._buffer.extend(bloque)

        # Separamos una respuesta completa del buffer
        posicion = self._buffer.index(b"\n")
        respuesta = bytes(self._buffer[:posicion])
        del self._buffer[:posicion + 1]

        return respuesta.decode("utf-8").rstrip("\r")

    def cerrar(self):
        """Cierra la conexion TCP."""
        self.conexion.close()

if __name__ == "__main__":

    equipo = Instrumento()

    try:
        # PRUEBA 1: IDENTIFICACION DEL OSCILOSCOPIO
        identificacion = equipo.preguntar("*IDN?")
        datos = parsear_idn(identificacion)

        assert datos is not None
        assert datos["modelo"] == "ADS3202"

        print("Prueba 1 OK: Identificacion del osciloscopio")
        print("Datos interpretados:", datos)


        # PRUEBA 2: CAMBIO DE ESTADO DEL CANAL CH2
        equipo.enviar(":CH2:DISPlay ON")

        estado = equipo.preguntar(":CH2:DISPlay?")

        assert estado == "ON"

        print("Prueba 2 OK: Comando enviado y estado verificado")


        # PRUEBA 3: COMANDO CON SALTO DE LINEA
        identificacion_2 = equipo.preguntar("*IDN?\n")

        assert identificacion_2 == identificacion

        print("Prueba 3 OK: Comando con salto de linea procesado")


        # PRUEBA 4: CONSULTA A UN CANAL INEXISTENTE
        respuesta = equipo.preguntar(":MEASUrement:CH3:FREQuency?")

        assert respuesta == "ERROR: comando desconocido"

        # Comprobamos que el ejercicio 1 rechace el error
        assert parsear_idn(respuesta) is None

        print("Prueba 4 OK: Canal inexistente detectado")


        # PRUEBA 5: MAGNITUD NO RECONOCIDA
        respuesta = equipo.preguntar(":MEASUrement:CH1:TEMP?")

        assert respuesta == "ERROR: comando desconocido"

        print("Prueba 5 OK: Magnitud desconocida")


        # PRUEBA 6: MEDICION DE FRECUENCIA
        respuesta = equipo.preguntar(":MEASUrement:CH1:FREQuency?")

        frecuencia = float(respuesta)

        # Debe ser un numero finito
        assert math.isfinite(frecuencia)

        # El simulador trabaja a 1000 Hz con +/- 0.5% de variacion
        assert 995.0 <= frecuencia <= 1005.0

        print("Prueba 6 OK: Frecuencia =", frecuencia, "Hz")


        # PRUEBA 7: CAMBIO DE ESTADO DEL CANAL
        equipo.enviar(":CH2:DISPlay OFF")

        assert equipo.preguntar(":CH2:DISPlay?") == "OFF"

        equipo.enviar(":CH2:DISPlay ON")

        assert equipo.preguntar(":CH2:DISPlay?") == "ON"

        print("Prueba 7 OK: Cambio de estado CH2")


        # PRUEBA 8: COMANDO CON TIPO DE DATO INCORRECTO
        try:
            equipo.enviar(123)

        except TypeError:
            print("Prueba 8 OK: Se detecto comando no valido")

        else:
            assert False, "No se detecto el error de tipo"


        # PRUEBA 9: IDENTIFICACION DEL MULTIMETRO
        multimetro = Instrumento(puerto=5556)

        try:
            respuesta = multimetro.preguntar("*IDN?")

            datos_multimetro = parsear_idn(respuesta)

            assert datos_multimetro is not None
            assert datos_multimetro["modelo"] == "XDM1041"

            print("Prueba 9 OK: Multimetro identificado")

        finally:
            multimetro.cerrar()
    finally:
        equipo.cerrar()
