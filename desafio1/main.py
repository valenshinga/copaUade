import csv  #libreria para archivos .csv
import os

class Consulta:
    """
    Clase para manejar la consulta de preguntas y respuestas.
    """
    def __init__(self, pregunta, respuesta):
        self.pregunta = pregunta
        self.respuesta = respuesta

    def __str__(self):
        return f"Pregunta: {self.pregunta}, Respuesta: {self.respuesta}"

def abrir_csv():
    """
    Abre el archivo CSV y devuelve una lista de objetos Consulta.
    """
    opciones = []
    directorio_actual = os.path.dirname(os.path.abspath(__file__))  # Obtener el directorio actual
    path = os.path.join(directorio_actual, "preguntas.csv")  # Crear la ruta del archivo CSV
    with open(path, "r", newline="", encoding='utf-8') as archivo_csv:
        csvReader = csv.reader(archivo_csv)
        next(csvReader)  # Saltear la primera fila que es el encabezado
        for columna in csvReader:
            # print(columna[0], ":", columna[1])  # Imprimir cada pregunta y respuesta
            opciones.append(Consulta(columna[0], columna[1]))  # Agregar cada pregunta y respuesta a la lista de opciones
    return opciones  # Devolver la lista de opciones

def listar_opciones(opciones):
    """
    Imprime las opciones disponibles.
    """
    print("-> Las preguntas disponibles son:")
    for i, opcion in enumerate(opciones):
        print(f"{i + 1}. {opcion.pregunta}")

def obtener_respuesta(opciones, preguntaIndex):
    """
    Busca la respuesta a una pregunta en la lista de opciones.
    """
    print(f"-> Buscando respuesta para la pregunta {preguntaIndex}...")
    print(f"{len(opciones)} opciones disponibles.")
    if preguntaIndex > len(opciones):
        return None
    return opciones[preguntaIndex - 1].respuesta

def registrar_opcion(opciones):
    """
    Registra una nueva opción en el archivo CSV.
    """
    nueva_pregunta = input("-> Escribí la pregunta que querés registrar: \n")
    respuesta_pregunta = input("-> Escribí la respuesta esperada a esa pregunta, si es que la sabés. Sino, clickea 'Enter': \n")
    with open("preguntas.csv", "a", newline="", encoding='utf-8') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow([nueva_pregunta, respuesta_pregunta])
    opciones.append(Consulta(nueva_pregunta, respuesta_pregunta))  # Agregar la nueva opción a la lista de opciones

preguntasRespuestas = abrir_csv()   #diccionario para almacenar preguntas y respuestas

print("-> ¡Hola! Soy un asistente virtual, ¿en qué puedo ayudarte?")
requiereOpciones = input("-> Si no sabés qué preguntar, podés ver las preguntas disponibles escribiendo 'opciones'")
if (requiereOpciones == "opciones"):
    listar_opciones(preguntasRespuestas)  # Imprimir las opciones disponibles
preguntaUsuario = ""  # Variable para almacenar la pregunta del usuario
while preguntaUsuario != "salir":     #bucle principal
    preguntaUsuario = input("-> Ingresá el número de la pregunta (ingresá 'salir' para salir): \n")
    if preguntaUsuario == "salir":
        break
    respuesta = obtener_respuesta(preguntasRespuestas, int(preguntaUsuario)) #busca la respuesta a la pregunta
    print(f"-> respuesta... {respuesta}")
    if respuesta == "":
        print("-> No tengo respuesta para esa pregunta, ¿querés registrarla?")
        continue
    elif respuesta:
        print("-> ",respuesta)
        continue
    else:   #Pregunta NO esta registrada
        agregarPregunta = input("-> Esa pregunta no está registrada, ¿querés registrarla? (si/no): \n")
        if agregarPregunta in {"si","Si","sí","Sí","s","y"}: #si se quiere ingresar una respuesta para la pregunta no resgitrada
            registrar_opcion(preguntasRespuestas)
            print("-> Respuesta registrada, ¡gracias!")
        else:   #si no se quiere ingresar una respuesta para la pregunta no registrada
            print("-> No hay problema, ¡preguntame otra cosa!")
print("-> ¡Chau!")