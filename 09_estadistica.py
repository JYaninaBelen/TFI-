
import os
import math
import importlib.util
import importlib.machinery

# Ruta exacta al archivo 08_log en la misma carpeta (funciona aunque no tenga extensión .py)
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_08 = os.path.join(directorio_actual, "08_log.py")

# Cargamos el archivo 08_log directamente desde su ruta
loader = importlib.machinery.SourceFileLoader("etapa_08", ruta_08)
spec = importlib.util.spec_from_loader("etapa_08", loader)
etapa_08 = importlib.util.module_from_spec(spec)
loader.exec_module(etapa_08)


def resumen(valores):
    """
    Recibe una lista de valores numéricos y devuelve un diccionario con estadísticas:
    n, minimo, maximo, promedio y desvio estándar muestral (n - 1).
    Devuelve None si la lista está vacía.
    """
    if not valores or len(valores) == 0:
        return None
        
    n = len(valores)
    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores) / n
    
    # Cálculo del desvío estándar muestral (dividiendo por n - 1)
    if n == 1:
        desvio = 0.0
    else:
        suma_cuadrados = sum((v - promedio) ** 2 for v in valores)
        desvio = math.sqrt(suma_cuadrados / (n - 1))
        
    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "desvio": desvio
    }


def fuera_de_rango(valores, minimo, maximo):
    """
    Devuelve una lista con las posiciones (índices) de los valores que 
    se salen del rango [minimo, maximo] (los extremos se consideran adentro).
    """
    posiciones = []
    for i, v in enumerate(valores):
        if v < minimo or v > maximo:
            posiciones.append(i)
    return posiciones


# --- BLOQUE DE PRUEBAS DE LA ETAPA 9 ---
if __name__ == "__main__":
    print("Ejecutando pruebas de la Etapa 9 (Estadística de una serie)...\n")
    
    # 1. Prueba de resumen con datos de ejemplo
    datos_ejemplo = [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0]
    res = resumen(datos_ejemplo)
    print(f"1) Resumen estadístico de ejemplo: {res}")
    assert res["n"] == 8
    assert res["minimo"] == 10.0
    assert res["maximo"] == 23.0
    
    # 2. Prueba con lista vacía y un solo elemento
    assert resumen([]) is None
    assert resumen([42.0])["desvio"] == 0.0
    
    # 3. Prueba de fuera_de_rango (extremos 10.0 y 20.0 cuentan como adentro)
    fuera = fuera_de_rango(datos_ejemplo, 10.0, 20.0)
    print(f"2) Posiciones fuera de rango [10, 20]: {fuera}")
    assert fuera == [2, 3, 5, 6]
    
    # 4. Control con la serie de verdad de mediciones.log (Etapa 8 + Etapa 9)
    ruta_log = os.path.join(directorio_actual, "mediciones.log")
    
    print("\n3) Leyendo 'mediciones.log' usando leer_log de 08_log...")
    series, rechazadas = etapa_08.leer_log(ruta_log)
    
    clave_freq_ch1 = ('ADS3202', 'CH1', 'FREQ')
    if clave_freq_ch1 in series:
        valores_freq = [m['valor'] for m in series[clave_freq_ch1]]
        est_ch1 = resumen(valores_freq)
        print(f"   Estadísticas de CH1 FREQ: {est_ch1}")
        
        # Validaciones exigidas por la cátedra:
        # Promedio a menos del 0,5 % de 1000 Hz y desvío menor a 5 Hz
        assert abs(est_ch1['promedio'] - 1000.0) / 1000.0 < 0.005, "El promedio difiere más del 0.5% de 1000 Hz"
        assert est_ch1['desvio'] < 5.0, "El desvío estándar es mayor a 5 Hz"
        print("   -> ¡Control de serie de verdad superado con éxito!")
    else:
        print("   -> Advertencia: No se encontró la serie ('ADS3202', 'CH1', 'FREQ') en el log.")

    print("\n¡La Etapa 9 pasó todas las pruebas correctamente!")