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
    
    print(f"-> Contribuir")
    print(f"-> {'Atras' if atras else 'Salir'}")
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
    ruta_txt = obtener_ruta_archivo(nombre_txt)
    
    with open(ruta_txt, 'r') as archivo:
        lineas = archivo.readlines()
        
    dashes = (len(ruta_diccionario) + 1) * "-"
    if pregunta:
        nuevaLinea = f"{dashes}{pregunta}: {respuesta}\n"
    else:
        nuevaLinea =f"{dashes}{respuesta}\n" 
        
    cont = 1
    if ruta_diccionario:
        for indice, linea in enumerate(lineas):
            if linea == f"{cont * "-"}{ruta_diccionario[0]}\n":
                ruta_diccionario.pop(0)
                cont += 1
                if not ruta_diccionario:         
                    lineas[indice+1:indice+1] = nuevaLinea
                    break
    else:
        if not lineas[-1].endswith("\n"):
            lineas[-1] += "\n"
        lineas.append(nuevaLinea)
        
    with open(ruta_txt, 'w') as archivo:
        archivo.writelines(lineas)

    return leer_txt(nombre_txt)

def registrar_entrada(ruta_diccionario:list, nombre_archivo: str) -> dict:
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
                return 
            elif respuesta in (1,2):
                opcion = respuesta
                break
        elif "cancelar" in respuesta:
            print("-> adicion cancelada")
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

    return guardar_entrada(nombre_archivo,ruta_diccionario,respuesta,pregunta)


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
    
    agregar = False
    continuar = True
    if respuesta.isdigit():
        respuesta = int(respuesta)
        if 1 <= respuesta <= len(opciones):
            ruta_diccionario.append(opciones[respuesta - 1])
            print(f"-> Buenísimo, hablemos sobre el tema {ruta_diccionario[-1]} ¿Qué exactamente quieres saber?")
    elif "atras" in respuesta and ruta_diccionario:
        ruta_diccionario.pop()
    elif "salir" in respuesta:
        continuar = False
    elif "contribuir" in respuesta:
        agregar = True
    else:
        opciones_lower = [opcion.lower() for opcion in opciones]
        coinciden = [index for index, opcion in enumerate(opciones_lower) if opcion in respuesta]
        if not coinciden or len(coinciden) > 1:
            print("-> Perdón, no logré entenderte. Por favor seleccioná una opción devuelta.")
        else:
            ruta_diccionario.append(opciones[coinciden[0]])
            print(f"-> Buenísimo, hablemos sobre el tema {ruta_diccionario[-1]}. ¿Qué querés saber exactamente?")
    
    return agregar, continuar, ruta_diccionario

def main_loop(nombre_archivo: str) -> None:
    """Ejecuta el bucle principal del programa."""
    memoria = leer_txt(nombre_archivo)
    if not memoria:
        return
        
    ruta_diccionario = []
    print("-> ¡Hola! Soy la Pokedex, ¿en qué puedo ayudarte?")
    
    continuar = True
    while continuar:
        nivel_actual = memoria
        for clave in ruta_diccionario:
            nivel_actual = nivel_actual[clave]

        if isinstance(nivel_actual, dict):
            opciones = mostrar_opciones(nivel_actual, bool(ruta_diccionario))
            print("")
            respuesta = input("-> Ingrese una respuesta: ")
            agregar, continuar, ruta_diccionario = procesar_respuesta_usuario(respuesta, opciones, ruta_diccionario)
            if agregar:
                resultado = registrar_entrada(ruta_diccionario.copy(),nombre_archivo)
                if resultado: 
                    memoria = resultado
        else:
            print("")
            print(f"-> {ruta_diccionario.pop()}: {nivel_actual}")
            
    print("-> ¡Chau!")

if __name__ == "__main__":
    main_loop("preguntas.txt")