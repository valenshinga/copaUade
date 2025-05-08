import os

SALIR = {"salir", "SALIR", "Salir", "exit"}
OPCIONES = "opciones"
SI= {"si","Si","sí","Sí","s","y"}
NO= {"no","NO","No","n","N"}

# abre y guarda en memoria las preguntas y respuestas del csv
def abrir_txt(txtPath: str) -> dict:
    absolutePath = os.path.dirname(os.path.abspath(__file__)) 
    fullPath = os.path.join(absolutePath, txtPath)
    memoria = dict()    #un diccionario para tener en memoria
    #registrar las preguntas y respuestas en el diccionario
    with open(fullPath,"r", newline="",encoding='utf-8') as archivoTxt:
        temaActual = None 
        for linea in archivoTxt:
            if linea[0] != "-":
                temaActual = linea.strip()
                memoria[temaActual] = dict() #se guardan los temas en un diccionario
                continue
            pregunta, respuesta = linea.replace("-","").strip().split(":")
            memoria[temaActual][pregunta] = respuesta    #se registran las preguntas y respuestas del archivo "preguntas.csv" en el diccionario
    return memoria     

# muestra las preguntas del csv y devuelve las devuelve en una lista
def mostrar_opciones(memoria:dict)->list:
    print("-> Las preguntas que conozco son:")
    opciones = list(memoria.keys()) #se guardan las preguntas en una lista
    for index,key in enumerate(memoria.keys()):
        opciones.append(key)
        print(f"-> {index + 1} : {key}")
    return opciones

def mostrar_temas(memoria:dict)->list:
    print("-> Los temas que conozco son:")
    opciones = list(memoria.keys()) #se guardan los temas en una lista
    for index,key in enumerate(memoria.keys()):
        opciones.append(key)
        print(f"-> {index + 1} : {key}")
    return opciones
        
#solicita una respuesta a la pregunta y la agrega al csv
def registrar_pregunta(memoria:dict, pregunta:str, txtPath:str) -> None:
    respuesta = input("-> ¿Cual sería la respuesta esperada para esa pregunta?: ")
    absolutePath = os.path.dirname(os.path.abspath(__file__)) 
    fullPath = os.path.join(absolutePath, txtPath)

    with open(fullPath,"a", newline="",encoding='utf-8') as archivoTxt: #registra la respuesta a la pregunta
        archivoTxt.writerow([pregunta,respuesta])
    memoria[pregunta] = respuesta
    print("-> respuesta registrada, ¡gracias!")

def main_loop(txtPath:str) -> None: 
    
    memoria = abrir_txt(txtPath)

    print("-> ¡Hola! Soy un asistente virtual, ¿con qué puedo ayudarte?")
    mostrar_temas(memoria)
    tema_seleccionado = None
    while True:      
        if not tema_seleccionado:
            tema_seleccionado = input("-> Selecciona un tema (Escribí 'salir' para salir): ").strip()
            if tema_seleccionado in memoria:
                print(f"-> Has seleccionado el tema '{tema_seleccionado}'.")
            else:
                print("-> Tema no encontrado. Por favor, selecciona un tema válido.")
                continue
        
        print("-> Si no sabés qué preguntar, podés ver las preguntas disponibles escribiendo 'opciones'")
        preguntaUsuario = input("-> Ingrese una pregunta o 'opciones' (ingrese 'salir' para salir): ")
        
        if preguntaUsuario in SALIR: 
            break # si quiere salir
        elif preguntaUsuario == OPCIONES: #si elije mostrar las opcines
            opciones = mostrar_opciones(memoria)
            if not opciones:
                continue
            while True:
                opcionElegida = input("Ingrese el numero de la pregunta: ").strip()
                if opcionElegida.isdigit():
                    opcionElegida = int(opcionElegida)
                    if 1 <= opcionElegida <= len(opciones):
                        pregunta = opciones[opcionElegida - 1]
                        print(f"-> La respuesta a la pregunta '{pregunta}' es:")
                        print(f"-> {memoria[pregunta]}")
                        break
                    else:
                        print("-> Opción fuera de rango.")
                else:
                    print("-> Opción inválida. Por favor, ingrese un número.")
        elif preguntaUsuario in memoria:
            print(f"-> {memoria[preguntaUsuario]}")
        else:   #si la pregunta NO esta registrada
            preguntaDesconocida = input("-> No conozco esa pregunta ¿queres ingresar una respuesta a esa pregunta?: ")
            if preguntaDesconocida in SI: #si se quiere ingresar una respuesta para la pregunta no resgitrada
                registrar_pregunta(memoria,preguntaUsuario,txtPath)
            elif preguntaDesconocida not in NO: #si se ingresa algo raro
                print("-> No entiendo tu respuesta. Asumiré que no deseas registrar la pregunta.")
    print("-> ¡Chau!")


if __name__ == "__main__":
    main_loop("preguntas.txt")
