import os

def printear_error(error: str, mensaje_personalizado: str = "") -> None:
    """
    Imprime un mensaje de error.

    Args:
        error (str): Mensaje de error que se desea imprimir
        mensaje_personalizado (str): Mensaje personalizado que se desea imprimir
    """
    salida = f"{mensaje_personalizado}: {error}" if mensaje_personalizado else f"Error: {error}"
    print(salida)

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
        printear_error(str(e), f"No se encontró el archivo {nombre_txt}")
    except Exception as e:
        printear_error(str(e), "Error al leer el archivo")
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
    
    print(f"-> 0 : {'atras' if atras else 'salir'}")
    return opciones

def registrar_pregunta(memoria: dict, pregunta: str, txtPath: str) -> None:
    """Registra una nueva pregunta y respuesta en el archivo."""
    ruta_archivo = obtener_ruta_archivo(txtPath)
    
    try:
        with open(ruta_archivo, 'a', encoding='utf-8') as archivo:
            archivo.write(f"\n{pregunta}: ")
    except Exception as e:
        printear_error(str(e), "Error al registrar la pregunta")

def procesar_respuesta_usuario(respuesta: str, opciones: list, ruta_diccionario: list) -> tuple:
    """
    Procesa la respuesta del usuario y retorna si debe continuar y la ruta actualizada.
    
    Args:
        respuesta (str): Respuesta del usuario
        opciones (list): Lista de opciones disponibles
        ruta_diccionario (list): Ruta actual del diccionario

    Returns:
        tuple: Tupla con un booleano y la ruta actualizada
    """
    respuesta = respuesta.strip().lower()
    
    if respuesta.isdigit():
        respuesta = int(respuesta)
        if respuesta == 0:
            if ruta_diccionario:
                ruta_diccionario.pop()
            else:
                return False, ruta_diccionario
        elif 1 <= respuesta <= len(opciones):
            ruta_diccionario.append(opciones[respuesta - 1])
            print(f"-> Buenísimo, hablemos sobre el tema {ruta_diccionario[-1]} ¿Qué exactamente quieres saber?")
    elif "atras" in respuesta and ruta_diccionario:
        ruta_diccionario.pop()
    elif "salir" in respuesta:
        return False, ruta_diccionario
    else:
        opciones_lower = [opcion.lower() for opcion in opciones]
        coinciden = [index for index, opcion in enumerate(opciones_lower) if opcion in respuesta]
        if not coinciden or len(coinciden) > 1:
            print("-> Perdón, no logré entenderte. Por favor seleccioná una opción devuelta.")
        else:
            ruta_diccionario.append(opciones[coinciden[0]])
            print(f"-> Buenísimo, hablemos sobre el tema {ruta_diccionario[-1]}. ¿Qué querés saber exactamente?")
    
    return True, ruta_diccionario

def main_loop(nombre_archivo: str) -> None:
    """Ejecuta el bucle principal del programa."""
    memoria = leer_txt(nombre_archivo)
    if not memoria:
        return
        
    ruta_diccionario = []
    print("-> ¡Hola! Soy un asistente virtual, ¿en qué puedo ayudarte?")
    
    while True:
        nivel_actual = memoria
        for clave in ruta_diccionario:
            nivel_actual = nivel_actual[clave]

        if isinstance(nivel_actual, dict):
            opciones = mostrar_opciones(nivel_actual, bool(ruta_diccionario))
            print("")
            respuesta = input("-> Ingrese una pregunta (ingrese 'salir' para salir): ")
            
            continuar, ruta_diccionario = procesar_respuesta_usuario(respuesta, opciones, ruta_diccionario)
            if not continuar:
                break
        else:
            print("")
            print(f"-> {ruta_diccionario.pop()}  {nivel_actual}")
            
    print("-> ¡Chau!")

if __name__ == "__main__":
    main_loop("preguntas.txt")