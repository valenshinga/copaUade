import os
import json
import re
import random

INPUT_POOL = ["¿Sobre qué Pokémon quieres saber?  ", "¿Tienes algún Pokémon en mente?  ", "¿Qué información estás buscando?  ", "¿Qué Pokémon te interesa?  ", "¿Puedo ayudarte con algún Pokémon?  ","¡Pregúntame sobre cualquier Pokémon!  ","¿Quieres que te cuente algo de un Pokémon?  ","¿Y ahora qué quieres saber?  ","¿Cuál Pokémon te da curiosidad?  ","¿Qué te gustaría que te contara? "]
ERROR_POOL = ["Lo siento, hubo un error al procesar tu consulta. ¿Podrías intentarlo de nuevo?","Lo siento, algo salió mal. ¿Puedes intentar otra vez?","Hubo un problema al procesar tu solicitud. ¿Podrías probar de nuevo?","Parece que ocurrió un error. Inténtalo nuevamente, por favor."]
END_POOL = ["Gracias por usar la Pokedex. ¡Chau!", "Ha sido un placer ayudarte. ¡Adiós!", "¡Fue un gusto! ¡Hasta la próxima!", "Gracias por usar la Pokédex. ¡Nos vemos!","Gracias por tu consulta. ¡Que tengas un buen día!"]
NOT_FOUND_POOL = ["Lo siento, no pude encontrar información sobre ese Pokémon. ¿Podrías ser más específico?", "No tengo registro de ese Pokémon. ¿Estás seguro del nombre?","No pude reconocer ese Pokémon. ¿Podrías escribirlo de otra forma?","No logré identificar a ese Pokémon. ¿Podrías especificarlo mejor?"]
NOT_SURE_POOL = ["No estoy seguro de qué Pokémon buscas. ¿Podrías ser más específico?","No estoy seguro a cuál Pokémon te refieres. ¿Podrías aclararlo?","No me queda claro qué Pokémon querés consultar. ¿Podés explicarlo mejor?"]

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

def leer_json(nombre_json: str) -> dict:
    """
    Lee un archivo JSON y retorna su contenido como diccionario.
    
    Args:
        nombre_json (str): Nombre del archivo JSON a leer

    Returns:
        dict: Diccionario con el contenido del archivo JSON
    """

    ruta_archivo = obtener_ruta_archivo(nombre_json)
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo_json:
            return json.load(archivo_json)
    except FileNotFoundError as e:
        registrar_log_error([], "", f"No se encontró el archivo {nombre_json}")
    except json.JSONDecodeError as e:
        registrar_log_error([], "", f"Error al decodificar el JSON: {str(e)}")
    except Exception as e:
        registrar_log_error([], "", f"Error al leer el archivo: {str(e)}")
    return {}

def encontrar_pokemon(texto: str, pokemones: list) -> list:
    """
    Encuentra coincidencias de Pokémon en el texto del usuario usando regex.
    
    Args:
        texto (str): Texto ingresado por el usuario
        pokemones (list): Lista de Pokémon disponibles
        
    Returns:
        list: Lista de coincidencias encontradas con su puntuación
    """
    texto = texto.lower()
    coincidencias = []
    
    for pokemon in pokemones:
        nombre = pokemon["nombre"].lower()
        # Buscar coincidencias exactas
        if nombre in texto or texto in nombre:
            coincidencias.append((pokemon, 1.0))
            continue
            
        # Buscar coincidencias parciales solo si no hay coincidencias exactas
        if not coincidencias:
            # Crear un patrón regex que busque el nombre del Pokémon
            # con posibles errores de escritura o variaciones
            patron = f".*{nombre}.*"
            if re.search(patron, texto):
                coincidencias.append((pokemon, 0.9))
                continue
            
            # Buscar coincidencias por palabras individuales
            palabras_texto = set(texto.split())
            palabras_pokemon = set(nombre.split())
            
            # Si alguna palabra del Pokémon está en el texto
            if any(palabra in palabras_texto for palabra in palabras_pokemon):
                coincidencias.append((pokemon, 0.8))
    
    coincidencias.sort(key=lambda x: x[1], reverse=True)
    return coincidencias

def extraer_palabras_clave(texto: str) -> dict:
    """
    Extrae palabras clave del texto del usuario.
    
    Args:
        texto (str): Texto ingresado por el usuario
        
    Returns:
        dict: Diccionario con las palabras clave encontradas
    """
    texto = texto.lower()
    palabras_clave = {
        "pokemon": None,
        "tipo": False,
        "habilidad": False,
        "estadisticas": False,
        "altura": False,
        "peso": False
    }
    
    # Buscar mención de Pokémon
    if "pokemon" in texto or "pokémon" in texto:
        palabras_clave["pokemon"] = True
    
    # Buscar interés en tipos
    if any(palabra in texto for palabra in ["tipo", "tipos", "es de tipo", "es tipo"]):
        palabras_clave["tipo"] = True
    
    # Buscar interés en habilidades
    if any(palabra in texto for palabra in ["habilidad", "habilidades", "puede", "poder"]):
        palabras_clave["habilidad"] = True
    
    # Buscar interés en estadísticas
    if any(palabra in texto for palabra in ["estadisticas", "estadísticas", "stats", "puntos", "fuerza", "defensa"]):
        palabras_clave["estadisticas"] = True
    
    # Buscar interés en altura
    if any(palabra in texto for palabra in ["altura", "alto", "tamaño"]):
        palabras_clave["altura"] = True
    
    # Buscar interés en peso
    if any(palabra in texto for palabra in ["peso", "pesa", "masa"]):
        palabras_clave["peso"] = True
    
    return palabras_clave

def generar_respuesta(pokemon: dict, palabras_clave: dict) -> str:
    """
    Genera una respuesta basada en el Pokémon y las palabras clave.
    
    Args:
        pokemon (dict): Información del Pokémon
        palabras_clave (dict): Palabras clave encontradas
        
    Returns:
        str: Respuesta generada
    """
    respuesta = []
    
    if palabras_clave["tipo"]:
        tipos = ", ".join(pokemon["tipo"])
        respuesta.append(f"{pokemon['nombre']} es de tipo {tipos}.")
    
    if palabras_clave["habilidad"]:
        habilidades = []
        if "normal" in pokemon["habilidades"]:
            habilidades.extend(pokemon["habilidades"]["normal"])
        if "oculta" in pokemon["habilidades"]:
            habilidades.extend(pokemon["habilidades"]["oculta"])
        respuesta.append(f"Sus habilidades son: {', '.join(habilidades)}.")
    
    if palabras_clave["estadisticas"]:
        stats = pokemon["estadisticas"]
        respuesta.append(f"Sus estadísticas son: PS: {stats['ps']}, Ataque: {stats['atk']}, "
                       f"Defensa: {stats['def']}, Ataque Especial: {stats['atk_esp']}, "
                       f"Defensa Especial: {stats['def_esp']}, Velocidad: {stats['velocidad']}.")
    
    if palabras_clave["altura"]:
        respuesta.append(f"Su altura es de {pokemon['altura']} metros.")
    
    if palabras_clave["peso"]:
        respuesta.append(f"Su peso es de {pokemon['peso']} kilogramos.")
    
    if not respuesta:
        respuesta.append(f"¿Qué te gustaría saber sobre {pokemon['nombre']}? Puedo contarte sobre sus tipos, "
                       f"habilidades, estadísticas, altura o peso.")
    
    return " ".join(respuesta)

def registrar_pregunta_no_encontrada(pregunta: str, respuesta: str) -> None:
    """
    Registra una pregunta no encontrada y su respuesta en un archivo.
    
    Args:
        pregunta (str): Pregunta realizada por el usuario
        respuesta (str): Respuesta proporcionada
    """
    ruta_archivo = obtener_ruta_archivo("preguntas_no_encontradas.txt")
    
    try:
        with open(ruta_archivo, "a", encoding='utf-8') as archivo:
            archivo.write(f"Pregunta: {pregunta}\n")
            archivo.write(f"Respuesta: {respuesta}\n")
            archivo.write("-" * 50 + "\n")
    except Exception as e:
        registrar_log_error([], pregunta, f"Error al registrar pregunta no encontrada: {str(e)}")

def agregar_informacion_pokemon(pokemon: dict, tipo_info: str, valor: str) -> None:
    """
    Agrega nueva información sobre un Pokémon al archivo JSON.
    
    Args:
        pokemon (dict): Información del Pokémon
        tipo_info (str): Tipo de información a agregar
        valor (str): Valor de la información
    """
    ruta_archivo = obtener_ruta_archivo("preguntas.json")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        
        # Buscar el Pokémon en la lista
        for p in datos["pokemones"]:
            if p["nombre"] == pokemon["nombre"]:
                if tipo_info == "tipo":
                    p["tipo"] = valor.split(", ")
                elif tipo_info == "habilidad":
                    if "normal" not in p["habilidades"]:
                        p["habilidades"]["normal"] = []
                    p["habilidades"]["normal"].append(valor)
                elif tipo_info == "estadisticas":
                    stats = valor.split(", ")
                    p["estadisticas"] = {
                        "total": sum(int(s.split(": ")[1]) for s in stats),
                        "ps": int(stats[0].split(": ")[1]),
                        "atk": int(stats[1].split(": ")[1]),
                        "def": int(stats[2].split(": ")[1]),
                        "atk_esp": int(stats[3].split(": ")[1]),
                        "def_esp": int(stats[4].split(": ")[1]),
                        "velocidad": int(stats[5].split(": ")[1])
                    }
                elif tipo_info == "altura":
                    p["altura"] = float(valor)
                elif tipo_info == "peso":
                    p["peso"] = float(valor)
                break
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            
    except Exception as e:
        registrar_log_error([], "", f"Error al agregar información: {str(e)}")

def solicitar_informacion_faltante(pokemon: dict, tipo_info: str) -> None:
    """
    Solicita al usuario que ingrese información faltante sobre un Pokémon.
    
    Args:
        pokemon (dict): Información del Pokémon
        tipo_info (str): Tipo de información faltante
    """
    print(f"\n-> No tengo información sobre {tipo_info} de {pokemon['nombre']}.")
    print("-> ¿Te gustaría agregar esta información? (sí/no)")
    
    respuesta = input("-> ").strip().lower()
    if respuesta in ["si", "sí", "yes", "y"]:
        if tipo_info == "tipo":
            print("-> Ingresa los tipos separados por coma (ejemplo: Fuego, Volador):")
            valor = input("-> ").strip()
        elif tipo_info == "habilidad":
            print("-> Ingresa el nombre de la habilidad:")
            valor = input("-> ").strip()
        elif tipo_info == "estadisticas":
            print("-> Ingresa las estadísticas en el siguiente formato:")
            print("-> PS: X, Ataque: X, Defensa: X, Ataque Especial: X, Defensa Especial: X, Velocidad: X")
            valor = input("-> ").strip()
        elif tipo_info == "altura":
            print("-> Ingresa la altura en metros (ejemplo: 1.7):")
            valor = input("-> ").strip()
        elif tipo_info == "peso":
            print("-> Ingresa el peso en kilogramos (ejemplo: 90.5):")
            valor = input("-> ").strip()
        
        agregar_informacion_pokemon(pokemon, tipo_info, valor)
        print("-> ¡Gracias! La información ha sido agregada.")

def verificar_informacion_faltante(pokemon: dict, palabras_clave: dict) -> list:
    """
    Verifica qué información falta para el Pokémon según las palabras clave.
    
    Args:
        pokemon (dict): Información del Pokémon
        palabras_clave (dict): Palabras clave encontradas
        
    Returns:
        list: Lista de tipos de información que faltan
    """
    info_faltante = []
    
    if palabras_clave["tipo"] and not pokemon.get("tipo"):
        info_faltante.append("tipo")
    
    if palabras_clave["habilidad"] and not pokemon.get("habilidades"):
        info_faltante.append("habilidad")
    
    if palabras_clave["estadisticas"] and not pokemon.get("estadisticas"):
        info_faltante.append("estadisticas")
    
    if palabras_clave["altura"] and not pokemon.get("altura"):
        info_faltante.append("altura")
    
    if palabras_clave["peso"] and not pokemon.get("peso"):
        info_faltante.append("peso")
    
    return info_faltante

def registrar_nuevo_pokemon(nombre: str) -> dict:
    """
    Registra un nuevo Pokémon en la base de datos.
    
    Args:
        nombre (str): Nombre del nuevo Pokémon
        
    Returns:
        dict: Información del nuevo Pokémon registrado
    """
    ruta_archivo = obtener_ruta_archivo("preguntas.json")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        
        nuevo_pokemon = {
            "nombre": nombre,
            "tipo": [],
            "habilidades": {
                "normal": [],
                "oculta": []
            },
            "altura": "",
            "peso": "",
            "estadisticas": {
                "total": 0,
                "ps": 0,
                "atk": 0,
                "def": 0,
                "atk_esp": 0,
                "def_esp": 0,
                "velocidad": 0
            }
        }
        
        datos["pokemones"].append(nuevo_pokemon)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            
        return nuevo_pokemon
            
    except Exception as e:
        registrar_log_error([], nombre, f"Error al registrar nuevo Pokémon: {str(e)}")
        return None

def procesar_consulta(texto: str, memoria: dict) -> str:
    """
    Procesa la consulta del usuario y genera una respuesta.
    
    Args:
        texto (str): Texto ingresado por el usuario
        memoria (dict): Diccionario con la información de Pokémon
        
    Returns:
        str: Respuesta generada
    """
    palabras_clave = extraer_palabras_clave(texto)
    coincidencias = encontrar_pokemon(texto, memoria["pokemones"])
    
    if not coincidencias:
        palabras = texto.lower().split()
        for palabra in palabras:
            if palabra not in ["pokemon", "pokémon", "es", "de", "tipo", "tiene", "cuales", "son", "sus", "las", "los", "el", "la", "un", "una", "unos", "unas"]:
                print(f"\n-> No tengo información sobre {palabra.capitalize()}.")
                print("-> ¿Te gustaría registrarlo como nuevo Pokémon? (sí/no)")
                respuesta = input("-> ").strip().lower()
                
                if respuesta in ["si", "sí", "yes", "y"]:
                    nuevo_pokemon = registrar_nuevo_pokemon(palabra.capitalize())
                    if nuevo_pokemon:
                        print("-> ¡Excelente! Ahora puedes agregar información sobre este Pokémon.")
                        print("-> ¿Qué información te gustaría agregar primero? (tipo/habilidad/estadisticas/altura/peso)")
                        tipo_info = input("-> ").strip().lower()
                        solicitar_informacion_faltante(nuevo_pokemon, tipo_info)
                        memoria = leer_json("preguntas.json")
                        return f"¡{palabra.capitalize()} ha sido registrado! Puedes preguntarme sobre él en cualquier momento."
                break
        return random.choice(NOT_FOUND_POOL)
    
    pokemon, similitud = coincidencias[0]
    if similitud < 0.9:
        return random.choice(NOT_SURE_POOL)
    
    info_faltante = verificar_informacion_faltante(pokemon, palabras_clave)
    
    if info_faltante:
        for tipo_info in info_faltante:
            solicitar_informacion_faltante(pokemon, tipo_info)
            memoria = leer_json("preguntas.json")
            for p in memoria["pokemones"]:
                if p["nombre"] == pokemon["nombre"]:
                    pokemon = p
                    break
    
    return generar_respuesta(pokemon, palabras_clave)

def obtener_respuesta_aleatoria(pool:list):
    original = pool.copy()
    pendientes = []
    
    while True:
        if not pendientes:
            pendientes = original[:]
            random.shuffle(pendientes)
        yield f"\n-> {pendientes.pop()}"

def main_loop(nombre_archivo: str) -> None:
    """
    Ejecuta el bucle principal del programa.

    Args:
        nombre_archivo (str): Nombre del archivo JSON a leer

    Returns:
        None: El programa finaliza cuando el usuario decide salir
    """
    try:
        memoria = leer_json(nombre_archivo)
        if not memoria:
            registrar_log_error([], "", "No se pudo cargar el archivo de memoria")
            return
            
        print("-> ¡Hola! Soy la Pokedex, ¿en qué puedo ayudarte?")
        print("-> Puedes preguntarme sobre cualquier Pokémon de la primera generación.")
        print("-> Por ejemplo: '¿Qué tipo es Charmander?' o '¿Cuáles son las habilidades de Pikachu?'")
        print("-> Escribe 'salir' para terminar.")
        
        continuar = True
        inputGenerator = obtener_respuesta_aleatoria(INPUT_POOL)
        errorGenerator = obtener_respuesta_aleatoria(ERROR_POOL)
        while continuar:
            try:
                respuesta = input(next(inputGenerator)).strip()
                if respuesta.lower() == "salir":
                    continuar = False
                    continue
                
                registrar_log_info([], respuesta, "consulta")
                resultado = procesar_consulta(respuesta, memoria)
                if "ha sido registrado" in resultado:
                    memoria = leer_json("preguntas.json")
                print(f"-> {resultado}")
                
            except Exception as e:
                registrar_log_error([], respuesta, f"Error inesperado: {str(e)}")
                print(next(errorGenerator))
                
    except Exception as e:
        registrar_log_error([], "", f"Error fatal al iniciar el chatbot: {str(e)}")
    finally:
        print(f"-> {random.choice(END_POOL)}")

if __name__ == "__main__":
    main_loop("preguntas.json")
