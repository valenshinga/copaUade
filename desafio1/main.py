import csv  #libreria para archivos .csv
import os

SALIR = {"salir", "SALIR", "Salir", "exit"}
OPCIONES = "opciones"
Si= {"si","Si","sí","Sí","s","y"}
NO= {"no","NO","No","n","N"}

# abre y guarda en memoria las preguntas y respuestas del csv
def abrir_csv(csvPath: str) -> dict:
    absolutePath = os.path.dirname(os.path.abspath(__file__)) 
    fullPath = os.path.join(absolutePath, csvPath)
    memoria = dict()    #un diccionario para tener en memoria
    #registrar las preguntas y respuestas en el diccionario
    with open(fullPath,"r", newline="",encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile)
        next(csvReader) #saltear la primera fila que es el encabezado
        for row in csvReader:
            memoria[row[0]] = row[1]    #se registran las preguntas y respuestas del archivo "preguntas.csv" en el diccionario
    return memoria     
 
# muestra las preguntas del csv y devuelve las devuelve en una lista
def mostrar_opciones(memoria:dict)->list:
    print("-> Las preguntas que conozco son:")
    opciones = list(memoria.keys()) #se guardan las preguntas en una lista
    for index,key in enumerate(memoria.keys()):
        opciones.append(key)
        print(f"-> {index + 1} : {key}")
    return opciones
        
#solicita una respuesta a la pregunta y la agrega al csv
def registrar_pregunta(memoria:dict, pregunta:str, csvPath:str) -> None:
    respuesta = input("-> ¿Cual sería la respuesta esperada para esa pregunta?: ")
    absolutePath = os.path.dirname(os.path.abspath(__file__)) 
    fullPath = os.path.join(absolutePath, csvPath)

    with open(fullPath,"a", newline="",encoding='utf-8') as csvfile: #registra la respuesta a la pregunta
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow([pregunta,respuesta])
    memoria[pregunta] = respuesta
    print("-> respuesta registrada, ¡gracias!")

def main_loop(csvPath:str) -> None: 
    
    memoria = abrir_csv(csvPath)
    
    print("-> ¡Hola! Soy un asistente virtual, ¿en qué puedo ayudarte?")
    print("-> Si no sabés qué preguntar, podés ver las preguntas disponibles escribiendo 'opciones'")
    while True:     
        respuesta = input("-> Ingrese una pregunta o 'opciones' (ingrese 'salir' para salir): ")
        
        if respuesta in SALIR: 
            break # si quiere salir
        elif respuesta == OPCIONES: #si elije mostrar las opcines
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
        elif respuesta in memoria:
            print(f"-> {memoria[respuesta]}")
        else:   #si la pregunta NO esta registrada
            respuesta2 = input("-> No conozco esa pregunta ¿queres ingresar una respuesta a esa pregunta?: ")
            if respuesta2 in Si: #si se quiere ingresar una respuesta para la pregunta no resgitrada
                registrar_pregunta(memoria,respuesta,csvPath)
            elif respuesta2 not in NO: #si se ingresa algo raro
                print("-> No entiendo tu respuesta. Asumiré que no deseas registrar la pregunta.")
    print("-> ¡Chau!")


if __name__ == "__main__":
    main_loop("preguntas.csv")
