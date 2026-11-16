EL prompt inicial de las consulta de los puntos  1-4 y 8-10 fue el siguiente :

Hola, soy estudiante de telecomunicaciones, primer año, cursando actualmente la materia de programacion, en el trabajo final nos pidieron desarrollar un codigo
para un banco de mediciones automatizado, o sea una computadora que le habla a un instrumento de laboratorio, le pide mediciones, verifica que esas mediciones tengan sentido y escribe el informe.

El lenguaje es python, Sólo la biblioteca estándar. Nada de pip install . Todo lo que necesitás — socket , math. Ya viene con Python.
Con respecto al instrumento de medicion, este es el contexto:

Vos no tenés el osciloscopio en tu casa. Por eso la cátedra te entrega instrumento_virtual.py : un programa que hace de cuenta que es el osciloscopio ADS3202 y el multímetro XDM1041 del laboratorio, y que contesta los mismos comandos que contestan los equipos de verdad.
Se abre una terminal y se escribe:

python3 instrumento_virtual.py

El programa queda escuchando y no devuelve el cursor. Eso está bien: es un instrumento prendido. Desde otra terminal corrés tu programa. Para apagarlo, Ctrl+C .
Equipo                  Dirección   Puerto
ADS3202 — osciloscopio  127.0.0.1   5555
XDM1041 — multímetro    127.0.0.1   5556

El protocolo elegido para la comunucacion es SCPI, el por que es el siguiente:

Un instrumento de medición moderno — un osciloscopio, un analizador de espectro, un multímetro — no se usa sólo con la perilla. Se lo controla desde una computadora, y se lo controla con SCPI.

SCPI significa Standard Commands for Programmable Instruments. Es de principios de los noventa, se apoya en la norma IEEE 488.2, y hoy lo entienden equipos de fabricantes que no se hablan entre ellos.

Cómo se lee un comando SCPI: Los comandos están organizados como un árbol, de lo general a lo particular, separando los niveles con dos puntos:

:MEASUrement:CH1:FREQuency?

se lee: medición → canal 1 → frecuencia → preguntar.

El signo de pregunta al final es lo que más importa. Con ? es una consulta: el instrumento contesta algo. Sin ? es una orden: el instrumento hace algo y no contesta nada.
:CH1:DISPlay ON  <- orden: prendé el canal 1
:CH1:DISPlay?    <- consulta: ¿el canal 1 está prendido?

En el software de la cátedra esos dos casos son dos botones distintos, ENVIAR y QUERY.
En tu programa van a ser dos funciones distintas, enviar y preguntar .

3 Reglas sobre el instrumento virtual:

-No se modifica. El archivo se entrega tal cual está. El instrumento es lo que se mide, no lo que se ajusta. Un grupo que cambia el instrumento para que su programa dé bien está haciendo lo contrario de medir.

-No se copia adentro de tus archivos. Va suelto en el repositorio, con el nombre que tiene.

-Tiembla a propósito. Cada vez que le preguntás una medición te contesta un número un poco distinto, igual que un instrumento real.

Fin de contexto del instrumento virtual.

El programa esta dividido en 10 partes, para poder escribirlo de a poco y de forma modular


1 — Identificación
2 — Magnitudes
3 — Órdenes y consultas
4 — Configurar un canal
5 — El cliente
6 — El barrido
7 — La verificación
8 — El registro
9 — Estadística
10 — El informe

1- Identificacion:

Prompt: Necesito hacer una funcion donde se reciba el texto (*IDN?), esta funcion tiene que devolver un diccionario con las siguientes claves: "fabricante, modelo, serie y version". Agregar una condicional, si la respuesta no sirve, que devuelva "None".
Los campos TIENEN que estar separados por comas, y que solamente se muestren 4 campos, en caso de que hayan instrumentos que devuelvan 5 o mas campos.
Casos a tener en cuenta, campos < 4, cadena vacia, campos con espacios de mas alrededor y la espuesta ERROR: comando desconocido.


La IA devolvio una funcion excelente, pero le hicimos un cambio a una de las lineas:

if texto_limpio.upper().startswith("ERROR"):
        return None

fue cambiada por:

if "ERROR" in texto_limpio.upper():
        return None

En caso de que el texto no contenga la palabra ERROR al comienzo, no va a retornar None, en cambio con la correccion, no va a importar donde este, siempre va a retornar None

Se comprobo haciendo una consola interactiva que acepte INPUTS desde la terminal.




2- Magnitudes

Necesito 2 funciones, una que convierta notacion cientifica, ej "1.000000E+03", a, en este caso 1000.0 ,en caso de que la cadena de caracteres no sea un numero que devuelva "None". 

La otra funcion es una que haga el camino inverso y devuelva el texto que leeria un humano.

La regla es elegir el prefijo que deje el numero entre 1 y 999. Los prefijos soportados son, pico, nano, micro, mili, kilo, mega y giga.

A tener en cuenta: la segunda funcion (999.9999, "Hz") tiene que dar 1 kHz , no 1000 Hz . Tene en cuenta si vas a redonder, mirar de vuelta si coincide la unidad.

La IA devolvio un codigo funcional pero le cambiamos una linea que nos parecia compleja por algo mas sensillo y facil de digerir.


if not isinstance(texto, str):
        return None

por

 if type(texto) is not str:
        return None

Si bien las 2 hacen lo mismo, una comparacion de type nos parecio mas clara y directa

3- Ordenes y consultas:

Necesito una funcion que devuelva el booleano True si el comando termina en "?"
Necesito otra funcion que devuelva "None" si el comando esta bien formado, en caso de no estarlo que devuelva un texto indicando que tipo de error hay, los errores posibles son los siguientes:

Regla                                  Ejemplo que la rompe
No puede estar vacío                   ""
Empieza con : o con *                  CH1:DISPlay ON
No hay dos espacios seguidos   	       :CH1:DISPlay ON
Hay a lo sumo un ?             	       :CH1:DISPlay??
El ? va al final                       :CH1:DIS?Play
Una orden lleva un solo argumento      :CH1:SCALe 1 v
Una consulta no lleva argumento        :CH1:DISPlay ON?


La funcion que devolvio la IA nos parecio ideal y consideramos no cambiar ninguna linea

4- Configurar un canal

Necesito una funcion que devuelva una lista ; "canal, display, acoplamiento, sonda, escala", en ese orden. En caso del primer item, si no es CH1 o CH2 que devuelva None.

Ej:

comandos_de_canal("CH1", "ON", "DC", "10X", "1v")

tiene que devolver exactamente:
[":CH1:DISPlay ON",
":CH1:COUPling DC",
":CH1:PROBe 10X",
":CH1:SCALe 1v"]

Esta funcion tiene que pasar todos los comandos de la funcion "validar" del ejercicio 3

Al igual que en el punto 3, la IA nos devolvio una funcion concisa y bastante corta. Como dato de color tambien nos devolvio un bloque con la funcion del punto 3 para validar que los datos sean correctos.


Aca hicimos un cambio e introducimos un prompt diferente:

prompt 1:sos un experto en programación lenguaje python y excelente profesor con metodologías de pedagogia excelentes, haciendo entendible cualquier tema tanto para personas que conocen del tema como para personas que recien empiezan, vas a ayudarme a programar un trabajo practico, aunque tambien me vas a explicar las lineas y cualquier duda que me surja me vas a explicar de forma didactiva

prompt2: ahora te voy a pasar un tp y te voy a pedir ayuda en los puntos que yo te indique

prompt3:me darias mas pruebas "criticas" como para sugerir validaciones en las consultas

5- El cliente

Necesito una clase "Instrumento" con 3 metodos

1-enviar(comando) ------- manda una orden y no espera nada- es ENVIAR
2-preguntar(comando) ---- manda una consulta y devuelve la respuesta- es QUERY
3-cerrar() -------------- cierra la conexion

La direccion y el puerto por defecto son 127.0.0.1:5555
Cada comando que se envia y cada respuesta termina en un salto de linea, esto identifica donde termina un mensaje y empieza el siguiente.


El codigo devuelto por la IA contenia un pequeño error:

posicion = self._buffer.index(b"\n")
respuesta = bytes(self._buffer[:posicion])


del self._buffer[:posicion]

Cuando le preguntamos por eso, la IA respondio:

El programa lee la respuesta, pero se olvida de tirar a la basura el "enter" (\n) que marcaba el final.

Imagina que es una bandeja de entrada:

    El instrumento te manda un mensaje que termina con un punto (\n).

    Tú lees el mensaje y limpias la bandeja, pero dejas el punto viejo tirado justo al principio.

    Cuando haces una segunda pregunta, el programa ve ese punto viejo, cree que ya llegó la respuesta nueva (cuando en realidad es basura vieja), y se desincroniza todo.

Al faltarle el + 1 (:posicion + 1), el código borra el mensaje pero se deja el \n atascado en el búfer para la próxima vez.



del self._buffer[:posicion + 1]

El codigo fue corregido de la manera explayada arriba


-6 El barrido

Necesito una funcion que le pida al instrumento las 3 magnitudes de cada canal y devuelva una lista de diccionarios, uno por medicion, con el canal, la magnitud, la unidad, el texto crudo que devolvio el equipo y el valor ya convertido a numero


Los comandos son estos, y el ? de cada uno es obligatorio:
:MEASUrement:CH1:FREQuency?
:MEASUrement:CH1:PKPK?
:MEASUrement:CH1:CYCRms?

Para CH2 es igual cambiando el número. Con dos canales y tres magnitudes, barrer de‐
vuelve seis mediciones.
Si el instrumento contesta un error, el valor queda en None pero el texto crudo se
guarda igual: al que después lea el informe le sirve más saber qué contestó el equipo
que ver un casillero vacío.

La IA nos devolvio un codigo con un error bastante grave:

comando = f":MEASUrement:{canal}:{magnitud}?"

Esta usando la variable incorrecta, la IA nos dice;

la lista magnitudes, cada tupla tiene un propósito específico:

    magnitud: Para usar internamente en tu programa (guardar en el diccionario).

    nombre_scpi: El comando real que entiende el instrumento por protocolo SCPI.

    unidad: La unidad de medida.

Al equivocarte de variable en el f-string, el programa le envía al instrumento un comando con una sintaxis o nomenclatura incorrecta que el oscilador virtual no va a reconocer, devolviendo un error o sin responder.

se cambio la variable a la correcta:

comando = f":MEASUrement:{canal}:{nombre_scpi}?"


-7 La verificacion

Escribí a) vrms_teorico(vpp) , que devuelve el Vrms que le correspondería a una senoide
de esa tensión pico a pico, y None si el dato no tiene sentido; b) coincide(medido, teorico,
tolerancia) , que devuelve True si el valor medido cae dentro de la tolerancia relativa
del teórico, con 0.02 (2 %) por defecto; y c) verificar_canal(filas, canal) , que busca el
PKPK y el CYCRMS de ese canal en el resultado del barrido y devuelve un diccionario que
dice si coinciden.
El error relativo se calcula así:
error = |medido - teorico| / |teorico|


La IA nos devolvio el codigo con errores de logica:

En la primer funcion:

vrms = vpp / math.sqrt(2)

La IA respondio: 

Fórmula incorrecta: Se divide solo por math.sqrt(2) en lugar de (2 * math.sqrt(2)) esto calcula mal el valor eficaz (da el doble del Vrms real para una senoidal).

el codigo se cambio:

vrms = vpp / (2 * math.sqrt(2))

En la segunda funcion:

error_relativo < tolerancia

Desigualdad estricta (<) en lugar de menor o igual (<=). Si el error relativo es exactamente igual a la tolerancia, fallará injustamente.

se agrego el simbolo "=" al codigo.


-8 El registro de la sesion

El archivo mediciones.log que te da la cátedra es el registro real de una sesión del banco:

cada línea es una medición, con seis campos separados por espacios.

2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.000431E+03

Como todo registro de laboratorio,tiene basura adentro.

a) analizar_linea(linea) , que devuelve el par (medicion, motivo) — uno de los dos siempre es None —, y b) leer_log(ruta) , que recorre el archivo y devuelve las series de valores agrupadas por equipo, canal y magnitud, más la lista de las líneas que rechazó con el motivo y el número de línea.

Las reglas de validez, para que no haya dudas:
Se ignora                       Se rechaza
la línea en blanco              la que no tiene exactamente seis campos
la que empieza con #            la de hora imposible, tipo 25:61:00
                                la de canal que no es CH1 ni CH2
                                la de magnitud que no es FREQ, PKPK ni CYCRMS
                                la de valor que no se puede convertir a número
                                
                                
Ignorar y rechazar no son lo mismo. Una línea en blanco no es un problema; una línea
con un valor roto sí, y hay que poder decir cuál era y por qué.

La IA nos devolvio un codigo casi excelente, excepto por el siguiente error:


    medicion = {
        "fecha": fecha_str,
        "hora": hora_str,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud,
        "crudo": valor_str,
        
        # --- AQUÍ ESTÁ EL ERROR ---
        "valor": valor_str  # Se está guardando el string en lugar de valor_num
    }

El tipo de dato es incorrecto: Aunque el código anterior valida con éxito que el texto se puede convertir a número (float(valor_str)), al final guarda el texto original (valor_str) en la clave "valor", ignorando por completo la variable numérica (valor_num).

    Rompe los análisis posteriores: Cuando intentes hacer operaciones matemáticas (como promedios, cálculos de Vrms, máximos, mínimos o graficar los valores en tus scripts), Python arrojará un error de tipo (TypeError) o fallará en los cálculos porque estará intentando operar con cadenas de texto (str) en lugar de números (float).

La corrección:

Para solucionarlo, simplemente debes asignar la variable convertida (valor_num) a la clave "valor":

Se corrigio segun lo devuelto por la IA

-9 EStadistica de una serie


Escribí a) resumen(valores) , que devuelve un diccionario con n , minimo , maximo , promedio y desvio , o None si la lista está vacía; y b) fuera_de_rango(valores, minimo, maximo) , que devuelve las posiciones de los valores que se salen del rango. Los dos extremos del rango cuentan como adentro.

El desvío estándar de la muestra se calcula dividiendo por n - 1 :

desvio = raiz( suma((v - promedio)^2) / (n - 1) )

Con un solo valor eso dividiría por cero, así que en ese caso el desvío es 0.0 .

Control con la serie de verdad: corriendo resumen sobre la serie de frecuencias de
CH1 que sale de mediciones.log , el promedio tiene que caer a menos del 0,5 % de
1000 Hz y el desvío tiene que ser menor que 5 Hz. Si no da eso, el error está en el
ejercicio 8, no en éste.


La IA nos devolvio un codigo con una linea que nos parecio engorrosa al extremo:

return list(map(lambda t: t[0], filter(lambda t: not (minimo <= t[1] <= maximo), [(i, valores[i]) for i in range(len(valores))])))

La cambiamos por una mas facil de digerir

for i, v in enumerate(valores):
        if v < minimo or v > maximo:
            posiciones.append(i)
    return posiciones


-10 El informe

Escribí "armar_informe(idn, series, verificaciones)" , que devuelve el informe completo
como una sola cadena de texto: el instrumento identificado, una línea por serie con su "n" , su promedio, su mínimo y su máximo ya con unidades legibles, y el resultado de cada verificación.

Esta función no imprime nada y no abre ningún archivo. Recibe todo por parámetro y
devuelve texto. El print lo hace quien la llama. 


Una función que imprime no se puede probar con un assert : no devuelve nada que compa‐
rar. Una función que devuelve texto sí.

Separar calcular de mostrar es lo que hace que la última pieza del trabajo sea la más fácil de verificar en vez de la más difícil. Es la idea de función pura de la Unidad 5, usada para algo concreto.

Y al final, el programa completo: con el instrumento virtual prendido, 10_informe.py tiene que identificar el equipo, barrer los dos canales, verificarlos, leer el log, y escribir el informe en pantalla. Ese es el banco de mediciones terminado.


La IA nos devolvio un codigo con varios errores de tipeo, ej:

valores = [m['valr'] for m in mediiciones]

y un error de logica:

promedio = sum(valores) / len(series)

¿Por qué está mal?

    Confunde el total de series con el tamaño de una serie:

        len(series) cuenta cuántas series o claves diferentes hay en todo el diccionario (por ejemplo, si estás midiendo 4 cosas distintas —como CH1 FREQ, CH1 PKPK, CH2 FREQ, etc.—, len(series) valdrá 4).

        Sin embargo, n (o len(valores)) representa la cantidad de mediciones individuales que tiene esa serie específica (que podrían ser 50, 100 o las que arroje el instrumento).

    El resultado numérico queda destruido:
    Si intentas calcular el promedio sumando todos los valores de una serie (por ejemplo, sumas 100 muestras y te da 500) y lo divides entre la cantidad total de series del diccionario (digamos, 4), el resultado será 500 / 4 = 125, cuando el promedio real debería ser 500 / 100 = 5. Estás dividiendo entre un número totalmente incorrecto.

La solución correcta:

Para calcular correctamente el promedio de una lista de valores, debes dividir siempre entre la cantidad de elementos de esa misma lista (n o len(valores)):

promedio = sum(valores) / n.

Se corrigio acorde.
