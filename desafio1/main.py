import os


# abre y guarda en memoria las preguntas y respuestas del txt
def read_txt(filePath:str ) -> dict:
    
    #Hay que hacer todo esto porque no nos dejan usar archivos json 
    
    absolutePath = os.path.dirname(os.path.abspath(__file__)) 
    fullPath = os.path.join(absolutePath, filePath)
    with open(fullPath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    root = {}
    stack = [(0, root)]  # (nivel, diccionario actual)

    for line in lines:
        # Determinar el nivel por cantidad de "-"
        level = 0
        while line.startswith("-"):
            line = line[1:]
            level += 1
        line = line.strip()

        # Separar clave y valor si hay ":"
        if ":" in line:
            key, value = map(str.strip, line.split(":", 1))
        else:
            key, value = line, {}

        # Asegurar que el stack está en el nivel adecuado
        while stack and stack[-1][0] >= level:
            stack.pop()

        # Agregar el nuevo elemento al diccionario actual
        parent = stack[-1][1]
        if isinstance(value, dict):
            parent[key] = value
            stack.append((level, parent[key]))
        else:
            parent[key] = value

    return root

# muestra las preguntas del txt y devuelve las devuelve en una lista
def mostrar_opciones(memoria:dict,atras:bool = True)->list:
    print("")
    opciones = list() #se guardan las preguntas en una lista
    for index,key in enumerate(memoria.keys()):
        opciones.append(key)
        print(f"-> {index + 1} : {key}")
    if atras:
        print(f"-> 0 : atras")
    else:
        print(f"-> 0 : salir")
        
    return opciones
        
#solicita una respuesta a la pregunta y la agrega al txt
def registrar_pregunta(memoria:dict, pregunta:str, txtPath:str) -> None:
    pass

def main_loop(txtPath:str) -> None: 
    
    memoria = read_txt(txtPath)
    rutaDiccionario = []
    nivelActual = memoria
    print("-> ¡Hola! Soy un asistente virtual, ¿en qué puedo ayudarte?")
    while True:     
        nivelActual = memoria
        for clave in rutaDiccionario:
            nivelActual = nivelActual[clave]

        if isinstance(nivelActual,dict):    # si es un tema
            opciones = mostrar_opciones(nivelActual,bool(rutaDiccionario))
            print("")
            respuesta = input("-> Ingrese una pregunta (ingrese 'salir' para salir): ")
            respuesta = respuesta.strip().lower()
            if respuesta.isdigit(): #si se ingreso un numero
                respuesta = int(respuesta)
                if respuesta == 0:
                    if rutaDiccionario: #si es atras (no es el primer menu)
                        rutaDiccionario.pop()
                    else: #si es salir
                        break  
                elif (1 <= respuesta <= len(opciones)):
                    rutaDiccionario.append(opciones[respuesta - 1])
                    print(f"-> Genial hablemos sobre el tema {rutaDiccionario[-1]} ¿Qué exactamente quieres saber?")
                else:
                    print("-> Opción fuera de rango.")
            elif "atras" in respuesta and rutaDiccionario:  #si se ingreso atras y no es el primer menu
                rutaDiccionario.pop()  
            elif "salir" in respuesta: #si se ingreso salir
                break
            else:   #si se ingreso un texto, se buscan las palabras clave dentro de la respuesta
                opcionesLower = [opcion.lower() for opcion in opciones]
                coinciden = [index for index,opcion in enumerate(opcionesLower) if opcion in respuesta]
                if not coinciden or len(coinciden) > 1: #si no se encuentran coincidencias o se encuentran mas de una
                    print("-> Lo siento, no logre entenderte. Porfavor seleccione una opcion devuelta.")
                else:
                    rutaDiccionario.append(opciones[coinciden[0]])
                    print(f"-> Genial hablemos sobre el tema {rutaDiccionario[-1]} ¿Qué exactamente quieres saber?")
                    
        else:   #si es una pregunta final
            print("")
            print(f"-> {rutaDiccionario.pop()}  {nivelActual}")
            
        
        

    print("-> ¡Chau!")


if __name__ == "__main__":
    main_loop("preguntas.txt")

