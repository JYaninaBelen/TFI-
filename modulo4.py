def comandos_de_canal(canal: str, display: str, acoplamiento: str, sonda: str, escala: str) -> list[str] | None:
    """
    Recibe los parámetros de configuración de un canal del osciloscopio
    y devuelve la lista con los 4 comandos SCPI correspondientes.
    Devuelve None si el canal no es válido.
    """
    # 1. Validamos que el canal sea estrictamente CH1 o CH2
    if canal not in ["CH1", "CH2"]:
        return None

    # 2. Construimos y devolvemos la lista con las 4 órdenes en orden exacto
    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}"
    ]

#Se agregan las funciones del modulo 3 para probar que estas se integran correctamente "comandos_de_canal()" 
#def es_consulta(comando: str) -> bool:
    """Devuelve True si el comando termina en '?', False en caso contrario."""
    comando_limpio = comando.strip()
    return comando_limpio.endswith("?")


#def validar(comando: str) -> str | None:
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

# =====================================================================
# BLOQUE DE PRUEBAS PARA EL PUNTO 4
# =====================================================================
#if __name__ == "__main__":
    # Probamos generar los comandos para el CH1
    lista_comandos = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")
    
    print("--- Comandos generados ---")
    for cmd in lista_comandos:
        print(cmd)
        
    print("\n--- Verificando validez con el validador del Ejercicio 3 ---")
    todos_validos = True
    for cmd in lista_comandos:
        # Recordá que tu función validar() devuelve None si es válido, o un texto de error si falla
        error = validar(cmd) 
        if error is not None:
            print(f"❌ El comando '{cmd}' falló: {error}")
            todos_validos = False
        else:
            print(f"✅ Válido: {cmd}")
            
    if todos_validos:
        print("\n¡Excelente! Todos los comandos generados pasaron las reglas de validación.")