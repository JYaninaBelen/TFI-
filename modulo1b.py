def parsear_idn(respuesta):
    """
    Recibe la cadena de texto que devuelve el comando *IDN? de un instrumento
    y la convierte en un diccionario estructurado. Si la cadena no es válida,
    devuelve None.
    """
    # 1. Verificamos que el dato recibido sea efectivamente una cadena de texto (str)
    # y que no esté vacía ni compuesta solo por espacios en blanco.
    if type(respuesta) is not str or not respuesta.strip():
        return None

    # 2. Limpiamos espacios o saltos de línea (\n, \r) al principio y al final del texto.
    texto_limpio = respuesta.strip()

    # 3. Verificamos si el instrumento respondió con un mensaje de error en cualquier parte del texto.
    if "ERROR" in texto_limpio.upper():
        return None

    # 4. Separamos el texto en una lista usando la coma como delimitador.
    campos = texto_limpio.split(",")

    # 5. Si la lista tiene menos de 4 elementos, la respuesta está incompleta o mal formada.
    if len(campos) < 4:
        return None

    # 6. Recorremos los primeros 4 elementos y les quitamos los espacios sobrantes
    # alrededor de cada uno (por ejemplo, si vino " OWON , ADS3202 ").
    # Al tomar solo el rango [:4], descartamos automáticamente el 5to campo del multímetro.
    campos_limpios = [campo.strip() for campo in campos[:4]]

    # 7. Verificamos que ninguno de los 4 campos principales haya quedado vacío
    # (por ejemplo, si el instrumento mandó "OWON,,25470803,V1.2.0").
    if any(campo == "" for campo in campos_limpios):
        return None

    # 8. Armamos y devolvemos el diccionario con las claves solicitadas por la cátedra.
    return {
        "fabricante": campos_limpios[0],
        "modelo": campos_limpios[1],
        "serie": campos_limpios[2],
        "version": campos_limpios[3],
    }
    


# =====================================================================
# BLOQUE DE PRUEBAS (Opcional: sirve para verificar que todo funcione)
# =====================================================================
#if __name__ == "__main__":
    # Caso 1: Osciloscopio (4 campos)
    #print("Osciloscopio:", parsear_idn("OWON,ADS3202,25470803,V1.2.0\n"))
    
    # Caso 2: Multímetro (5 campos, el último se ignora)
    #print("Multímetro:", parsear_idn("OWON,XDM1041,25470803,V4.4.0,3"))
    
    # Caso 3: Respuesta con espacios extra alrededor de las comas
    #print("Con espacios:", parsear_idn("  OWON , ADS3202 , 25470803 , V1.2.0  "))
    
    # Caso 4: Error del instrumento
    #print("Error instrumento:", parsear_idn("ERROR: comando desconocido"))
    
    # Caso 5: Cadena vacía o con menos de 4 campos
    #print("Vacía:", parsear_idn("   "))
    #print("Incompleta:", parsear_idn("OWON,ADS3202,25470803"))

# =====================================================================
#CONSOLA INTERACTIVA PARA LA FUNCION "parsear_idn()"
# =====================================================================
#if __name__ == "__main__":
    print("--- Simulador interactivo de parseo *IDN? ---")
    print("Escribí una cadena para probar (o escribí 'salir' para terminar):\n")
    
    while True:
        # Pedimos al usuario que escriba un texto por consola
        entrada_usuario = input("Ingrese respuesta del instrumento: ")
        
        # Condición para salir del bucle
        if entrada_usuario.lower() == "salir":
            print("¡Salgo del programa de prueba!")
            break
            
        # Ejecutamos la función con lo que escribió el usuario
        resultado = parsear_idn(entrada_usuario)
        
        # Mostramos el resultado
        print(f"Resultado devuelto: {resultado}\n")