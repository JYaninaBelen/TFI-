
from datetime import datetime

def analizar_linea(linea):
    """
    Analiza una línea del archivo de log.
    Devuelve (medicion_dict, None) si es válida,
    (None, None) si se debe ignorar (vacía o comentario),
    o (None, motivo_str) si se rechaza por algún error.
    """
    if not isinstance(linea, str):
        return None, "Línea no válida"
        
    linea_limpia = linea.strip()
    
    # 1. Ignorar líneas en blanco o comentarios
    if not linea_limpia or linea_limpia.startswith("#"):
        return None, None
        
    # 2. Separar campos usando split() sin argumentos (maneja espacios y tabulaciones correctamente)
    campos = linea_limpia.split()
    
    # 3. Validar cantidad exacta de campos (deben ser 6)
    if len(campos) != 6:
        return None, f"Cantidad de campos incorrecta ({len(campos)} en lugar de 6)"
        
    fecha_str, hora_str, equipo, canal, magnitud, valor_str = campos
    
    # 4. Validar hora (formato HH:MM:SS válido)
    try:
        datetime.strptime(hora_str, "%H:%M:%S")
    except ValueError:
        return None, f"Hora inválida: {hora_str}"
        
    # 5. Validar canal (debe ser CH1 o CH2)
    if canal not in ["CH1", "CH2"]:
        return None, f"Canal inválido: {canal}"
        
    # 6. Validar magnitud (debe ser FREQ, PKPK o CYCRMS)
    if magnitud not in ["FREQ", "PKPK", "CYCRMS"]:
        return None, f"Magnitud inválida: {magnitud}"
        
    # 7. Validar conversión a número usando nuestra función a_numero (o float directo)
    try:
        #
        # valor_num = 02_magnitudes(valor_str)
        valor_num = float(valor_str)
        if valor_num is None:
            raise ValueError()
    except ValueError:
        return None, f"Valor no convertible a número: {valor_str}"
        
    # Si pasa todas las validaciones, construimos el diccionario de la medición
    medicion = {
        "fecha": fecha_str,
        "hora": hora_str,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud,
        "crudo": valor_str,
        "valor": valor_num
    }
    
    return medicion, None


def leer_log(ruta):
    """
    Lee un archivo de log línea por línea.
    Devuelve un diccionario con las mediciones agrupadas y una lista de rechazos con su número de línea y motivo.
    """
    agrupadas = {}
    rechazadas = []
    
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                medicion, motivo = analizar_linea(linea)
                
                if medicion is not None:
                    # Agrupamos por (equipo, canal, magnitud)
                    clave = (medicion["equipo"], medicion["canal"], medicion["magnitud"])
                    if clave not in agrupadas:
                        agrupadas[clave] = []
                    agrupadas[clave].append(medicion)
                elif motivo is not None:
                    # Si hubo un motivo de rechazo (distinto de ignorado), lo guardamos
                    rechazadas.append({
                        "numero_linea": numero_linea,
                        "linea": linea.strip(),
                        "motivo": motivo
                    })
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo de log en la ruta '{ruta}'.")
        
    return agrupadas, rechazadas


# --- BLOQUE DE PRUEBAS DE LA ETAPA 8 ---
if __name__ == "__main__":
    print("Ejecutando pruebas de la Etapa 8 (El registro de la sesión)...")
    
    # 1. Prueba de una línea válida estándar
    linea_ok = "2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.000431E+03"
    med, mot = analizar_linea(linea_ok)
    assert med is not None and mot is None
    assert med["valor"] == 1000.431
    
    # 2. Prueba de línea con hora imposible (debe rechazarse)
    linea_error_hora = "2026-09-08 25:61:00 ADS3202 CH1 FREQ 1000"
    med, mot = analizar_linea(linea_error_hora)
    assert med is None and mot is not None
    
    # 3. Prueba de línea en blanco (debe ignorarse silenciosamente -> ambos None)
    med, mot = analizar_linea("   \n")
    assert med is None and mot is None
    
    print("¡La Etapa 8 pasó todas las pruebas de análisis de líneas exitosamente!")

    
    # --- BLOQUE DE PRUEBA FINAL PARA LA ETAPA 8 ---
    #---EN CONJUNTO CON MEDICIONES.LOG
    import os

# Para localiza el archivo mediciones en la misma carpeta donde corre este script
ruta_archivo = os.path.join(os.path.dirname(__file__), "mediciones.log") if "__file__" in locals() else "mediciones.log"

series, rechazadas = leer_log(ruta_archivo)

print(f"\n¡Análisis finalizado con éxito!")
print(f"-> Series de mediciones válidas agrupadas: {len(series)}")
print(f"-> Líneas con errores rechazadas por el filtro: {len(rechazadas)}")

print("\nEjemplo de algunas líneas rechazadas detectadas correctamente:")
for r in rechazadas[:5]:
    print(f"  - Línea {r['numero_linea']}: '{r['linea']}'")
    print(f"    Motivo: {r['motivo']}\n")