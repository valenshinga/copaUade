# COPA DE ALGORITMIA Y PROGRAMACIÓN – UADE 2025
## Desafío 1

### Objetivo:

- Diseñar la estructura del asistente y almacenar preguntas/respuestas en archivos. 

## Nicho de las preguntas/respuestas

- Pokemon (https://es.wikipedia.org/wiki/Pok%C3%A9mon)


## Estructura

```
┌── main.py           # Archivo principal con la lógica del chatbot
├── preguntas.txt     # Base de datos de Pokémon en formato jerárquico
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

2. Navegar por las opciones:
   - Usar números para seleccionar opciones
   - Escribir el nombre exacto del Pokémon
   - Usar "atras" para volver al menú anterior
   - Usar "salir" para terminar el programa

3. Contribuir información:
   - Seleccionar "Contribuir" en cualquier menú
   - Elegir entre agregar un tema o una pregunta
   - Seguir las instrucciones para ingresar la información

## Funcionalidades Principales

### Navegación
- Sistema de menús jerárquicos
- Opción de volver atrás
- Búsqueda por nombre o número

### Contribución
- Agregar nuevos temas
- Agregar nuevas preguntas y respuestas
- Validación de entradas

### Sistema de Logs
- Registro de errores
- Registro de interacciones
- Registro de advertencias

## Formato de Datos

El archivo `preguntas.txt` utiliza un formato jerárquico con guiones para indicar niveles:
```
-Pokémon
--Nombre del Pokémon
---Tipo
---Habilidades
---Estadísticas
```

## Manejo de Errores

El programa incluye manejo de errores para:
- Entradas inválidas
- Errores de navegación
- Problemas de lectura/escritura de archivos
- Errores inesperados

## Contribución

Para contribuir al proyecto:
1. Selecciona "Contribuir" en el menú
2. Elige entre agregar un tema o una pregunta
3. Sigue las instrucciones para ingresar la información
4. La información se guardará automáticamente en el archivo

## Limitaciones

- Solo incluye Pokémon de la primera generación
- No permite modificar información existente
- No incluye imágenes
- No permite búsquedas avanzadas

## Autor

Desarrollado como parte del desafío 1 de la Copa UADE, por el equipo 15 - Git Gods.