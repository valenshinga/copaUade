# COPA DE ALGORITMIA Y PROGRAMACIÓN – UADE 2025
## Desafío 2

### Objetivo:

- Implentar respuestas segun palabras clave. 

## Nicho de las preguntas/respuestas

- Pokemon (https://es.wikipedia.org/wiki/Pok%C3%A9mon)


## Estructura

```
┌── main.py           # Archivo principal con la lógica del chatbot
├── preguntas.json     # Base de datos de Pokémon en formato json
└── log.txt          # Archivo de registro de interacciones y errores (No incluido en entrega)
```

## Requisitos

- Python 3.x
- No se requieren dependencias externas

## Uso

1. Ejecutar el programa:
```bash
#Windows
python main.py
```

```bash
#Ubuntu
python3 main.py
```

2. Uso del chatbot:
   - Escribir sobre que pokemon se quiere obtener la informacion y que se quiere saber de este
   - Usar "salir" para terminar el programa
   - Usar "clear" para borrar todas las liñeas de informacion y empezar de 0

3. Contribuir información:
   - Introduce el nombre de un pokemon inexistente
   - Elige que "Sí" si quieres agregarlo
   - Seguir las instrucciones para ingresar la información
   - La información se guardará automáticamente en el archivo

## Funcionalidades Principales

### Navegación
- Sistema de menús jerárquicos
- Opción de volver atrás
- Búsqueda por nombre o número

### Contribución
- Agregar nuevos pokemons e informacion de estos
- Validación de entradas

### Sistema de Logs
- Registro de errores
- Registro de interacciones
- Registro de advertencias

## Formato de Datos

El archivo `preguntas.json` utiliza el formato json para almacenar sus respectivos datos. 

## Manejo de Errores

El programa incluye manejo de errores para:
- Entradas inválidas
- Errores de navegación
- Problemas de lectura/escritura de archivos
- Errores inesperados

## Limitaciones

- Solo incluye Pokémon de la primera generación
- No permite modificar información existente
- No incluye imágenes
- No permite búsquedas avanzadas

## Autor

Desarrollado como parte del desafío 2 de la Copa UADE, por el equipo 15 - Git Gods.
