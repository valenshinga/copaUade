import csv  #libreria para archivos .csv
import os

# abre y guarda en memoria las preguntas y respuestas del csv
def abrir_csv(csvPath) -> None:
    directorio_actual = os.path.dirname(os.path.abspath(__file__)) 
    fullPath = os.path.join(directorio_actual, csvPath)
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
    opciones = list()
    for index,key in enumerate(memoria.keys()):
        opciones.append(key)
        print(f"-> {index + 1} : {key}")
    return opciones
        
def registrar_pregunta(memoria:dict, pregunta:str, csvPath:str) -> None:
    respuestaPregunta = input("-> ¿Cual sería la respuesta esperada para esa pregunta?: ")
    directorio_actual = os.path.dirname(os.path.abspath(__file__)) 
    fullPath = os.path.join(directorio_actual, csvPath)

    with open(fullPath,"a", newline="",encoding='utf-8') as csvfile: #registra la respuesta a la pregunta
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow([pregunta,respuestaPregunta])
    memoria[pregunta] = respuestaPregunta
    print("-> respuesta registrada, ¡gracias!")

def main_loop(csvPath:str) -> None: 
    memoria = abrir_csv(csvPath)
    
    print("-> ¡Hola! Soy un asistente virtual, ¿en qué puedo ayudarte?")
    print("-> Si no sabés qué preguntar, podés ver las preguntas disponibles escribiendo 'opciones'")
    while True:     
        r = input("""-> Ingrese una pregunta o "opciones" (ingrese "salir" para salir): """)
        if r in {"salir","SALIR","Salir","exit"}: break # si quiere salir
        elif r == "opciones": #si elije mostrar las opcines
            opciones = mostrar_opciones(memoria)
            opcionElegida = int(input("Ingrese el numero de la pregunta: "))
            while opcionElegida <= 0 or opcionElegida > len(opciones):
                opcionElegida = int(input("Opcion invalida. Ingrese el numero de la pregunta: "))
            print(f"-> La respuesta a la pregunta {opciones[opcionElegida - 1]} es:")
            print(f"-> {memoria[opciones[opcionElegida - 1]]}")
        elif r in memoria: #si la pregunta esta registrada
            print(f"-> {memoria[r]}")
        else:   #si la pregunta NO esta registrada
            r2 = input("-> No conozco esa pregunta ¿queres ingresar una respuesta a esa pregunta?: ")
            if r2 in {"si","Si","sí","Sí","s","y"}: #si se quiere ingresar una respuesta para la pregunta no resgitrada
                registrar_pregunta(memoria,r,csvPath)

    print("-> ¡Chau!")

if __name__ == "__main__":
    main_loop("preguntas.csv")