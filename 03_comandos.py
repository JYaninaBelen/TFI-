def es_consulta(comando: str) -> bool:
    """Devuelve True si el comando termina en '?', False en caso contrario."""
    comando_limpio = comando.strip()
    return comando_limpio.endswith("?")


def validar(comando: str) -> str | None:
    """
    Valida un comando SCPI según las reglas de sintaxis.
    Devuelve None si es válido, o un mensaje de error fijo si falla alguna regla.
    """
    # 1. No puede estar vacío (ni contener solo espacios)
    if not comando or comando.strip() == "":
        return "ERROR: El comando no puede estar vacío."

    # Quitamos espacios sobrantes solo en los extremos para analizar
    cmd = comando.strip()

    # 2. Empieza con ':' o con '*'
    if not (cmd.startswith(":") or cmd.startswith("*")):
        return "ERROR: El comando debe comenzar con ':' o '*'."

    # 3. No hay dos espacios seguidos
    if "  " in cmd:
        return "ERROR: El comando no puede tener dos espacios seguidos."

    # 4. Hay a lo sumo un '?'
    cantidad_interrogacion = cmd.count("?")
    if cantidad_interrogacion > 1:
        return "ERROR: El comando puede tener como máximo un signo '?'."

    # 5. El '?' va al final
    if cantidad_interrogacion == 1 and not cmd.endswith("?"):
        return "ERROR: El signo '?' debe ubicarse únicamente al final."

    # Separamos el comando por espacios para analizar argumentos
    partes = cmd.split(" ")

    # 6. Una consulta no lleva argumento
    if es_consulta(cmd):
        if len(partes) > 1:
            return "ERROR: Una consulta no puede llevar argumentos."
    # 7. Una orden lleva como máximo un argumento (o exactamente uno según el caso)
    else:
        if len(partes) > 2:
            return "ERROR: Una orden puede llevar un solo argumento."
#Aunque parezca redundantes los pasos 6 y 7, son diferentes.
    # Si pasó todos los filtros, el comando es válido
    return None

#if __name__ == "__main__":
    pruebas = [
        ("", "Vacío"),
        ("CH1:DISPlay ON", "Sin : o * al inicio"),
        (":CH1:DISPlay  ON", "Doble espacio"),
        (":CH1:DISPlay??", "Doble ?"),
        (":CH1:DIS?Play", "? en el medio"),
        (":CH1:SCALe 1 v", "Dos argumentos en orden"),
        (":CH1:DISPlay ON?", "Argumento en consulta"),
        (":CH1:DISPlay ON", "Orden válida"),
        (":CH1:DISPlay?", "Consulta válida"),
        ("*IDN?", "Consulta IEEE 488.2 válida"),
    ]

    for cmd, descripcion in pruebas:
        resultado = validar(cmd)
        estado = "VÁLIDO" if resultado is None else resultado
        print(f"[{descripcion}] '{cmd}' -> {estado}")

# =====================================================================
# CONSOLA INTERACTIVA PARA PRUEBAS FUNCION "es_consulta()" y funcion "validar()"
# =====================================================================
if __name__ == "__main__":
    print("--- Validador interactivo de comandos SCPI ---")
    print("Ingresá un comando para probar (o escribí 'salir' para terminar).\n")
    
    while True:
        entrada = input("Ingrese comando SCPI: ")
        
        # Condición para salir del bucle
        if entrada.lower() == "salir":
            print("¡Saliendo del programa de prueba. Hasta luego!")
            break
            
        # Validamos el comando ingresado usando tu función
        resultado_error = validar(entrada)
        
        # Si validar devuelve None, el comando es correcto
        if resultado_error is None:
            print(" -> [VÁLIDO] El comando es correcto.\n")
        else:
            # Si devuelve un texto, ese texto es el error detectado
            print(f" -> [INVÁLIDO] {resultado_error}\n")
