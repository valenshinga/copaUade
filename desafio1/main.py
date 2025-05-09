import os


# Abre y guarda en memoria las preguntas y respuestas del txt
def read_txt( nombre_txt:str ) -> dict:
    """
    Lee un archivo de texto y lo convierte en un diccionario jerárquico.

    El archivo debe tener un formato específico donde:
    - Los niveles se indican con guiones ("-") al inicio de la línea
    - Los pares clave-valor (pregunta-respuesta) se separan con ":"
    - Las líneas sin ":" se tratan como temas padres con diccionarios vacíos como valor

    Args:
        nombre_txt (str): Nombre del archivo de texto a leer

    Returns:
        dict: Diccionario jerárquico construido a partir del contenido del archivo

    Ejemplo de formato del archivo:
        tema1: respuesta1
        -subtema1: subrespuesta1
        -subtema2: subrespuesta2
        --subsubtema1: subsubrespuesta1
    """
    
    path_absoluto = os.path.dirname(os.path.abspath(__file__)) 
    ruta_archivo = os.path.join(path_absoluto, nombre_txt)

    # Lee el archivo y formatea linea por linea
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo_txt:
        lineas = [linea.strip() for linea in archivo_txt if linea.strip()]

    # Inicializa el diccionario raíz y la pila para manejar la jerarquía
    root = {}
    stack = [(0, root)]  # Tupla (nivel, diccionario actual)

    for linea in lineas:
        # Cuenta el número de guiones para determinar el nivel
        nivel = 0
        while linea.startswith("-"):
            linea = linea[1:]
            nivel += 1
        linea = linea.strip()

        # Procesa la línea según si tiene ":" o no
        if ":" in linea:
            key, value = map(str.strip, linea.split(":", 1))
        else:
            key, value = linea, {}  # Si no hay ":", es un tema padre

        # Ajusta la pila al nivel correcto
        while stack and stack[-1][0] >= nivel:
            stack.pop()

        # Agrega el nuevo elemento al diccionario padre actual
        parent = stack[-1][1]
        if isinstance(value, dict):
            parent[key] = value
            stack.append((nivel, parent[key]))
        else:
            parent[key] = value
    
    return root

# muestra las preguntas del txt y las devuelve en una lista
def mostrar_opciones( memoria:dict, atras:bool = True ) -> list:
    print("")
    opciones = list() #se guardan las preguntas en una lista
    for indice, key in enumerate(memoria.keys()):
        opciones.append(key)
        print(f"-> {indice + 1} : {key}")
    if atras:
        print(f"-> 0 : atras")
    else:
        print(f"-> 0 : salir")
        
    return opciones
        
#solicita una respuesta a la pregunta y la agrega al txt
def registrar_pregunta(memoria:dict, pregunta:str, txtPath:str) -> None:
    pass

def main_loop(nombre_archivo:str) -> None:
    """
    Ejecuta el bucle principal del programa que permite la navegación interactiva por un árbol de preguntas y respuestas.

    Args:
        nombre_archivo (str): Ruta al archivo de texto que contiene la estructura de preguntas y respuestas.

    Returns:
        None: La función no retorna ningún valor, solo maneja la interacción con el usuario.
    """
    # Carga la estructura de datos desde el archivo
    memoria = read_txt(nombre_archivo)
    # Lista que mantiene el registro de la ruta actual en el árbol
    ruta_diccionario = []
    # Referencia al nivel actual en el árbol
    nivel_actual = memoria
    
    print("-> ¡Hola! Soy un asistente virtual, ¿en qué puedo ayudarte?")
    
    while True:
        # Navega hasta el nivel actual usando la ruta almacenada
        nivel_actual = memoria
        for clave in ruta_diccionario:
            nivel_actual = nivel_actual[clave]

        if isinstance(nivel_actual,dict):    # Si el nivel actual es un tema (tiene sub-opciones)
            # Muestra las opciones disponibles en el nivel actual
            opciones = mostrar_opciones(nivel_actual,bool(ruta_diccionario))
            print("")
            respuesta = input("-> Ingrese una pregunta (ingrese 'salir' para salir): ")
            respuesta = respuesta.strip().lower()
            
            if respuesta.isdigit(): # Si la respuesta es un número
                respuesta = int(respuesta)
                if respuesta == 0:
                    if ruta_diccionario: # Si hay niveles previos, retrocede
                        ruta_diccionario.pop()
                    else: # Si está en el nivel raíz, sale del programa
                        break  
                elif (1 <= respuesta <= len(opciones)):
                    # Avanza al siguiente nivel seleccionado
                    ruta_diccionario.append(opciones[respuesta - 1])
                    print(f"-> Buenísimo, hablemos sobre el tema {ruta_diccionario[-1]} ¿Qué exactamente quieres saber?")
                else:
                    print("-> Opción fuera de rango.")
            elif "atras" in respuesta and ruta_diccionario:  # Maneja el comando "atras"
                ruta_diccionario.pop()  
            elif "salir" in respuesta: # Maneja el comando "salir"
                break
            else:   # Busca coincidencias de palabras clave en la respuesta
                opciones_lower = [opcion.lower() for opcion in opciones]
                coinciden = [index for index,opcion in enumerate(opciones_lower) if opcion in respuesta]
                if not coinciden or len(coinciden) > 1: # Si no hay coincidencias únicas
                    print("-> Perdón, no logré entenderte. Por favor seleccioná una opción devuelta.")
                else:
                    ruta_diccionario.append(opciones[coinciden[0]])
                    print(f"-> Buenísimo, hablemos sobre el tema {ruta_diccionario[-1]}. ¿Qué querés saber exactamente?")
                    
        else:   # Si es una respuesta final, la muestra y retrocede un nivel
            print("")
            print(f"-> {ruta_diccionario.pop()}  {nivel_actual}")
    print("-> ¡Chau!")


if __name__ == "__main__":
    main_loop("preguntas.txt")

