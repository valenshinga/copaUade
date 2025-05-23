import os

def registrar_log_error(ruta: list, respuesta: str, error: str) -> None:
    """
    Registra un mensaje de error en el archivo de log.

    Args:
        ruta (list): Ruta del usuario
        respuesta (str): Respuesta del usuario
        error (str): Mensaje de error de python
    """
    ruta_archivo = obtener_ruta_archivo("log.txt")
    ruta_usuario = " -> ".join(ruta) if ruta else "inicio"
    linea = f"[ERROR] Ruta: {ruta_usuario} | Respuesta: {respuesta} | Error: {error}\n"
    
    with open(ruta_archivo, "a", encoding='utf-8') as archivo_log:
        archivo_log.write(linea)

def registrar_log_info(ruta: list, respuesta: str, accion: str) -> None:
    """
    Registra un mensaje de información en el archivo de log.

    Args:
        ruta (list): Ruta del usuario
        respuesta (str): Respuesta del usuario
        accion (str): Acción del usuario
    """
    ruta_archivo = obtener_ruta_archivo("log.txt")
    ruta = " -> ".join(ruta) if ruta else "inicio"
    linea = f"[INFO] Ruta: {ruta} | Respuesta: {respuesta} | Acción: {accion}\n"
    
    with open(ruta_archivo, "a", encoding='utf-8') as archivo_log:
        archivo_log.write(linea)

def registrar_log_advertencia(ruta: list, respuesta: str, mensaje: str) -> None:
    """
    Registra un mensaje de advertencia en el archivo de log.

    Args:
        ruta (list): Ruta del usuario
        respuesta (str): Respuesta del usuario
        mensaje (str): Mensaje de advertencia
    """
    ruta_archivo = obtener_ruta_archivo("log.txt")
    ruta = " -> ".join(ruta) if ruta else "inicio"
    linea = f"[WARNING] Ruta: {ruta} | Respuesta: {respuesta} | Mensaje: {mensaje}\n"
    
    with open(ruta_archivo, "a", encoding='utf-8') as archivo_log:
        archivo_log.write(linea)

def obtener_ruta_archivo(nombre_txt: str) -> str:
    """
    Obtiene la ruta absoluta del archivo.

    Args:
        nombre_txt (str): Nombre del archivo de texto a leer

    Returns:
        str: Ruta absoluta del archivo
    """
    path_absoluto = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path_absoluto, nombre_txt)

def procesar_linea(linea: str) -> tuple:
    """
    Procesa una línea del archivo y retorna su nivel, clave y valor.

    Args:
        linea (str): Línea del archivo que se está procesando

    Returns:
        tuple: Tupla con el nivel, clave y valor
    """
    nivel = 0
    while linea.startswith("-"):
        linea = linea[1:]
        nivel += 1
    linea = linea.strip()
    
    if ":" in linea:
        key, value = map(str.strip, linea.split(":", 1))
    else:
        key, value = linea, {}
        
    return nivel, key, value

def construir_diccionario(lineas: list) -> dict:
    """
    Construye el diccionario jerárquico a partir de las líneas procesadas.

    Args:
        lineas (list): Lista de líneas del archivo de texto

    Returns:
        dict: Diccionario jerárquico construido a partir del contenido del archivo .txt
    """
    root = {}
    stack = [(0, root)]

    for linea in lineas:
        nivel, key, value = procesar_linea(linea)
        
        while stack and stack[-1][0] >= nivel:
            stack.pop()

        parent = stack[-1][1]
        if isinstance(value, dict):
            parent[key] = value
            stack.append((nivel, parent[key]))
        else:
            parent[key] = value
    
    return root

def leer_txt(nombre_txt: str) -> dict:
    """
    Lee un archivo de texto y lo convierte en un diccionario jerárquico.
    
    Args:
        nombre_txt (str): Nombre del archivo de texto a leer

    Returns:
        dict: Diccionario jerárquico construido a partir del contenido del archivo .txt
    """
    ruta_archivo = obtener_ruta_archivo(nombre_txt)
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo_txt:
            lineas = [linea.strip() for linea in archivo_txt if linea.strip()]
        return construir_diccionario(lineas)
    except FileNotFoundError as e:
        registrar_log_error([], "", f"No se encontró el archivo {nombre_txt}")
    except Exception as e:
        registrar_log_error([], "", "Error al leer el archivo")
    return {}

def mostrar_opciones(memoria: dict, atras: bool = True) -> list:
    """
    Muestra las opciones disponibles y retorna una lista de ellas.

    Args:
        memoria (dict): Diccionario jerárquico que contiene las opciones disponibles
        atras (bool): Indica si se debe mostrar la opción de volver atrás

    Returns:
        list: Lista de opciones disponibles
    """
    print("")
    opciones = list(memoria.keys())
    
    for indice, key in enumerate(opciones, 1):
        print(f"-> {indice} : {key}")
    
    print(f"-> Contribuir")
    print(f"-> {'Atras' if atras else 'Salir'}")
    print(f"{'-> Inicio' if atras else ''}")
    return opciones

def guardar_entrada(nombre_txt:str, ruta_diccionario:list, respuesta:str, pregunta:str = None) -> dict:
    """Sigue en el archivo la ruta de diccionario para agregar un tema o una pregunta
    Args:
        nombre_txt (str): Nombre del archivo txt a modificar
        ruta_diccionario (list): Ruta actual del diccionario
        respuesta (str) : Puede ser el nombre del tema o la respuesta a una pregunta
        pregunta (str) : la pregunta en caso de que se quiera ingresar una pregunta

    Returns:
        dict: nuevo diccionario memoria con el cambio realizado 
    """   
    try:
        ruta_txt = obtener_ruta_archivo(nombre_txt)
        with open(ruta_txt, 'r') as archivo:
            lineas = archivo.readlines()
        
        dashes = (len(ruta_diccionario) + 1) * "-"
        nuevaLinea = f"{dashes}{pregunta}: {respuesta}\n" if pregunta else f"{dashes}{respuesta}\n"
        
        cont = 1
        if ruta_diccionario:
            for indice, linea in enumerate(lineas):
                if linea == f"{cont * '-'}{ruta_diccionario[0]}\n":
                    ruta_diccionario.pop(0)
                    cont += 1
                    if not ruta_diccionario:         
                        lineas[indice+1:indice+1] = [nuevaLinea]
                        break
        else:
            if not lineas[-1].endswith("\n"):
                lineas[-1] += "\n"
            lineas.append(nuevaLinea)
        
        with open(ruta_txt, 'w') as archivo:
            archivo.writelines(lineas)

        return leer_txt(nombre_txt)
    except IOError as e:
        registrar_log_error(ruta_diccionario, "", f"Error al guardar en el archivo: {str(e)}")
        return {}
    
def registrar_entrada(ruta_diccionario: list, nombre_archivo: str) -> dict:
    """Registra un nuevo tema o una nueva pregunta y respuesta en el archivo.
    Args:
        nombre_archivo (str): Nombre del archivo txt a modificar
        ruta_diccionario (list): Ruta actual del diccionario

    Returns:
        dict: nuevo diccionario memoria con el cambio realizado 
    """    
    print("-> Genial ¿qué queres agregar exactamente?\n")
    print("-> 0 : Cancelar")
    print("-> 1 : Tema")
    print("-> 2 : Pregunta")
    
    respuesta = input("-> Ingrese una respuesta: ")
    respuesta = respuesta.strip().lower()
    opcion = 0
    while not opcion:
        if respuesta.isdigit():
            respuesta = int(respuesta)
            if respuesta == 0:
                print("-> adicion cancelada")        
                registrar_log_info(ruta_diccionario, str(respuesta), "cancelar")
                return 
            elif respuesta in (1,2):
                opcion = respuesta
                break
        elif "cancelar" in respuesta:
            print("-> adicion cancelada")
            registrar_log_info(ruta_diccionario, respuesta, "cancelar")
            return
        elif "tema" in respuesta:
            opcion = 1
            break
        elif "pregunta" in respuesta:
            opcion = 2
            break
        print("-> Perdón, no logré entenderte ¿Podrías intentar devuelta?")
        respuesta = input("-> Ingrese una respuesta: ")
    
    if opcion == 1:
        respuesta = input("-> ¿Cúal es el nombre de este nuevo tema?: ")
        while respuesta.isdigit():
            respuesta = input("-> No puedes ingresar un numero como nombre. Por favor intenta otro nombre: ")
        pregunta = ""
    else:
        pregunta = input("-> ¿Cúal es la pregunta que quieres ingresar?: ")
        while pregunta.isdigit():
            pregunta = input("-> No puedes ingresar un numero como pregunta. Por favor intenta devuelta: ")
        respuesta = input("-> ¿Cúal es la respuesta a esa pregunta?: ")

    return guardar_entrada(nombre_archivo, ruta_diccionario, respuesta, pregunta)

def procesar_respuesta_numerica(respuesta: int, opciones: list, ruta_diccionario: list, nivel_actual: dict) -> tuple:
    """
    Procesa una respuesta numérica del usuario.
    
    Args:
        respuesta (int): Número ingresado por el usuario
        opciones (list): Lista de opciones disponibles
        ruta_diccionario (list): Ruta actual del diccionario
        nivel_actual (dict): Diccionario actual en el que estamos navegando

    Returns:
        tuple: (agregar, continuar, ruta_diccionario)
    """
    try:
        if 1 <= respuesta <= len(opciones):
            ruta_diccionario.append(opciones[respuesta - 1])
            siguiente_nivel = ruta_diccionario[-1]
            if isinstance(nivel_actual[siguiente_nivel], dict):
                print(f"-> Buenísimo, hablemos sobre {siguiente_nivel}. ¿Qué querés saber exactamente?")
        else:
            registrar_log_advertencia(ruta_diccionario, str(respuesta), "Número de opción fuera de rango")
            print("-> No pude entender tu respuesta. Por favor ingresá el número de la opción que querés elegir, o escribí el nombre exacto.")
        return False, True, ruta_diccionario
    except (KeyError, IndexError) as e:
        registrar_log_error(ruta_diccionario, str(respuesta), str(e))
        return False, True, ruta_diccionario[:-1] if ruta_diccionario else []

def procesar_respuesta_texto(respuesta: str, opciones: list, ruta_diccionario: list, nivel_actual: dict) -> tuple:
    """
    Procesa una respuesta de texto del usuario.
    
    Args:
        respuesta (str): Texto ingresado por el usuario
        opciones (list): Lista de opciones disponibles
        ruta_diccionario (list): Ruta actual del diccionario
        nivel_actual (dict): Diccionario actual en el que estamos navegando

    Returns:
        tuple: (agregar, continuar, ruta_diccionario)
    """
    try:
        match respuesta:
            case "inicio":
                return False, True, []
            case "atras" if ruta_diccionario:
                ruta_diccionario.pop()
                return False, True, ruta_diccionario
            case "salir":
                return False, False, ruta_diccionario
            case "contribuir":
                return True, True, ruta_diccionario
        
        opciones_lower = [opcion.lower() for opcion in opciones]
        coinciden = [index for index, opcion in enumerate(opciones_lower) if opcion in respuesta]
        
        if not coinciden or len(coinciden) > 1:
            registrar_log_advertencia(ruta_diccionario, respuesta, "Respuesta no reconocida")
            print("-> No pude entender tu respuesta. Por favor ingresá el número de la opción que querés elegir, o escribí el nombre exacto.")
            return False, True, ruta_diccionario
        
        ruta_diccionario.append(opciones[coinciden[0]])
        if isinstance(nivel_actual[ruta_diccionario[-1]], dict):    
            print(f"-> Buenísimo, hablemos sobre {ruta_diccionario[-1]}. ¿Qué querés saber exactamente?")
        return False, True, ruta_diccionario
    except (KeyError, IndexError) as e:
        registrar_log_error(ruta_diccionario, respuesta, str(e))
        return False, True, ruta_diccionario[:-1] if ruta_diccionario else []

def procesar_respuesta_usuario(respuesta: str, opciones: list, ruta_diccionario: list, nivel_actual: dict) -> tuple:
    """
    Procesa la respuesta del usuario y retorna si debe continuar y la ruta actualizada.
    
    Args:
        respuesta (str): Respuesta del usuario
        opciones (list): Lista de opciones disponibles
        ruta_diccionario (list): Ruta actual del diccionario
        nivel_actual (dict): Diccionario actual en el que estamos navegando

    Returns:
        tuple: Tupla con un booleano indicando si quiere contribuir, si debe continuar y la ruta actualizada
    """
    respuesta = respuesta.strip().lower()
    
    if respuesta.isdigit():
        return procesar_respuesta_numerica(int(respuesta), opciones, ruta_diccionario, nivel_actual)
    return procesar_respuesta_texto(respuesta, opciones, ruta_diccionario, nivel_actual)

def main_loop(nombre_archivo: str) -> None:
    """
    Ejecuta el bucle principal del programa.

    Args:
        nombre_archivo (str): Nombre del archivo txt a leer que contiene la información para el chatbot

    Returns:
        None: El programa finaliza cuando el usuario decide salir
    """
    try:
        memoria = leer_txt(nombre_archivo)
        if not memoria:
            registrar_log_error([], "", "No se pudo cargar el archivo de memoria")
            return
            
        ruta_diccionario = []
        print("-> ¡Hola! Soy la Pokedex, ¿en qué puedo ayudarte?")
        
        continuar = True
        while continuar:
            try:
                nivel_actual = memoria
                for clave in ruta_diccionario:
                    nivel_actual = nivel_actual[clave]

                if isinstance(nivel_actual, dict):
                    opciones = mostrar_opciones(nivel_actual, bool(ruta_diccionario))
                    print("")
                    respuesta = input("-> Ingrese una respuesta: ")
                    registrar_log_info(ruta_diccionario, respuesta, "navegacion")
                    agregar, continuar, ruta_diccionario = procesar_respuesta_usuario(respuesta, opciones, ruta_diccionario, nivel_actual)
                    if agregar:
                        resultado = registrar_entrada(ruta_diccionario.copy(), nombre_archivo)
                        if resultado: 
                            memoria = resultado
                else:
                    print("")
                    print(f"-> {ruta_diccionario.pop()}: {nivel_actual}")
            except KeyError as e:
                registrar_log_error(ruta_diccionario, "", f"Error al navegar por el diccionario: {str(e)}")
                ruta_diccionario = ruta_diccionario[:-1] if ruta_diccionario else []
            except Exception as e:
                registrar_log_error(ruta_diccionario, "", f"Error inesperado: {str(e)}")
                ruta_diccionario = ruta_diccionario[:-1] if ruta_diccionario else []
    except Exception as e:
        registrar_log_error([], "", f"Error fatal al iniciar el chatbot: {str(e)}")
    finally:
        print("-> Gracias por usar la Pokedex. ¡Chau!")

if __name__ == "__main__":
    main_loop("preguntas.txt")
