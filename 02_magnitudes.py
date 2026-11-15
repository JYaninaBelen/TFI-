import math


def a_numero(texto):
    """
    Convierte una cadena de texto (como '1.000000E+03') en un número flotante (float).
    Devuelve None si el texto no es un número válido o es infinito/NaN.
    """
    # 1. Verificamos que la entrada sea una cadena de texto.
    if type(texto) is not str:
        return None

    # 2. Quitamos espacios o saltos de línea alrededor del texto.
    texto_limpio = texto.strip()

    # 3. Si quedó vacío, no es un número.
    if texto_limpio == "":
        return None

    # 4. Intentamos convertir el texto a float. Python entiende notación científica
    # automáticamente (por ejemplo, float("1.000000E+03") da 1000.0).
    try:
        numero = float(texto_limpio)
    except ValueError:
        # Si el texto era "ERROR" o letras, fallará la conversión y devolvemos None.
        return None

    # 5. En Python, float("nan") o float("inf") son válidos pero no son mediciones reales.
    # math.isfinite() verifica que sea un número real finito.
    if not math.isfinite(numero):
        return None

    return numero


def con_unidad(valor, unidad):
    """
    Recibe un número flotante y una unidad base (ej. 'Hz', 'V', 's') y devuelve
    una cadena formateada con el prefijo métrico adecuado entre 1 y 999.
    """
    # 1. Caso especial: si el valor es exactamente cero, no lleva prefijo.
    if valor == 0:
        return f"0 {unidad}"

    # 2. Guardamos el signo por si nos pasan un voltaje negativo (ej. -0.707 V)
    # y trabajamos con el valor absoluto para calcular la escala.
    signo = "-" if valor < 0 else ""
    magnitud = abs(valor)

    # 3. Definimos la tabla de prefijos desde el más pequeño (pico) al más grande (Giga),
    # junto con su exponente en base 10.
    prefijos = [
        (-12, "p"),
        (-9,  "n"),
        (-6,  "u"),
        (-3,  "m"),
        (0,   ""),
        (3,   "k"),
        (6,   "M"),
        (9,   "G"),
    ]

   # 4. Buscamos el índice del prefijo comparando el número
    indice = 4  # Por defecto asumimos el índice de la unidad base (exponente 0, si está en el medio de la lista)
    
    # Recorremos la lista de prefijos en orden (de menor a mayor)
    for i, (exp, simbolo) in enumerate(prefijos):
        # Si nuestra magnitud es mayor o igual a 10 elevado a este exponente...
        if magnitud >= (10 ** exp):
            indice = i  # Actualizamos el índice con el mejor candidato encontrado

    # 6. Escalamos el número dividiéndolo por 10 elevado al exponente del índice elegido.
    escalado = magnitud / (10 ** prefijos[indice][0])

    # 7. Redondeamos a 3 decimales para limpiar ruido de punto flotante.
    redondeado = round(escalado, 3)

    # 8. CASO BORDE CLAVE: Si al redondear el número llegó a 1000 (ej. 999.9999 -> 1000.0)
    # y todavía tenemos un prefijo más grande disponible en la lista, subimos un escalón.
    if redondeado >= 1000 and indice < len(prefijos) - 1:
        indice += 1
        escalado = magnitud / (10 ** prefijos[indice][0])
        redondeado = round(escalado, 3)

    # 9. Formateamos el número para quitar ceros decimales innecesarios
    # (ej. 2.0 pasa a "2", 2.500 pasa a "2.5").
    numero_texto = f"{redondeado:g}"

    # 10. Obtenemos el símbolo del prefijo elegido (ej. "k", "m" o "").
    prefijo_elegido = prefijos[indice][1]

    # 11. Armamos y devolvemos el texto final respetando el espacio antes de la unidad.
    return f"{signo}{numero_texto} {prefijo_elegido}{unidad}"

# =====================================================================
# BLOQUE DE PRUEBAS
# =====================================================================
#if __name__ == "__main__":
    print("--- Pruebas a_numero ---")
    print("Notación científica:", a_numero("1.000000E+03"))
    print("Con espacios/salto:", a_numero("  -7.070000E-01\n"))
    print("Texto inválido:", a_numero("ERROR: comando desconocido"))
    print("Vacío:", a_numero(""))

    print("\n--- Pruebas con_unidad ---")
    print("1000.0 Hz   ->", con_unidad(1000.0, "Hz"))
    print("2500.0 Hz   ->", con_unidad(2500.0, "Hz"))
    print("2.0 V       ->", con_unidad(2.0, "V"))
    print("0.707 V     ->", con_unidad(0.707, "V"))
    print("0.0005 s    ->", con_unidad(0.0005, "s"))
    print("0.0 V       ->", con_unidad(0.0, "V"))
    print("999.9999 Hz ->", con_unidad(999.9999, "Hz"))


# =====================================================================
# CONSOLA INTERACTIVA PARA PRUEBAS FUNCION "a_numero()"
# =====================================================================
#if __name__ == "__main__":
    print("--- Probador interactivo de a_numero() ---")
    print("Escribí un valor para probar (o escribí 'salir' para terminar):\n")
    
    while True:
        # Pedimos input al usuario por consola
        entrada = input("Ingrese texto a convertir: ")
        
        # Condición para salir del bucle
        if entrada.lower() == "salir":
            print("¡Saliendo del programa de prueba. Hasta luego!")
            break
            
        # Llamamos a tu función con lo que ingresó el usuario
        resultado = a_numero(entrada)
        
        # Mostramos el resultado y el tipo de dato que devolvió
        print(f" -> Resultado: {resultado} (Tipo de dato: {type(resultado).__name__})\n")

# =====================================================================
# CONSOLA INTERACTIVA PARA PRUEBAS FUNCION "con_unidad()"
# =====================================================================
#if __name__ == "__main__":
    print("--- Simulador interactivo de con_unidad() ---")
    print("Ingresá un valor numérico y su unidad (o escribí 'salir' para terminar).\n")
    
    while True:
        # Pedimos el valor numérico
        entrada_valor = input("Ingrese el valor (ej: 0.0035 o 1500000) o 'salir': ")
        
        # Condición para salir del bucle
        if entrada_valor.lower() == "salir":
            print("¡Saliendo del programa de prueba. Hasta luego!")
            break
            
        # Intentamos convertir el valor ingresado a float de forma segura
        try:
            valor_numerico = float(entrada_valor)
        except ValueError:
            print(" ❌ Error: Ingrese un número válido.\n")
            continue
            
        # Pedimos la unidad base
        unidad_base = input("Ingrese la unidad (ej: V, Hz, A, s): ")
        
        # Ejecutamos la función y mostramos el resultado
        resultado = con_unidad(valor_numerico, unidad_base)
        print(f"Resultado formateado: --> {resultado}\n" + "-"*40)