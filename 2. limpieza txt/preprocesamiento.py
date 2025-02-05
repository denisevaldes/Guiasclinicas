"""
script que procesa archivos de texto en un directorio, eliminando saltos de página,
convirtiendo a minúsculas y eliminando espacios extra.
"""
import re
import os

# Función para limpiar el texto
def limpiar_texto(texto):
    # Eliminar saltos de página
    texto = re.sub(r'--- Página \d+ ---', '', texto)
    # Convertir a minúsculas
    texto = texto.lower()
    # Eliminar espacios extra
     # Eliminar líneas vacías
    texto = '\n'.join([linea for linea in texto.splitlines() if linea.strip() != ''])

    return texto

# Función para procesar archivos en un directorio
def procesar_archivos_en_directorio(directorio_entrada, directorio_salida):
    # Verificar si el directorio de entrada existe
    if not os.path.exists(directorio_entrada):
        print(f"El directorio de entrada {directorio_entrada} no existe.")
        return

    # Crear el directorio de salida si no existe
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        print(f"Directorio de salida {directorio_salida} creado.")

    # Recorrer todos los archivos en el directorio de entrada
    for nombre_archivo in os.listdir(directorio_entrada):
        # Construir la ruta completa del archivo de entrada
        ruta_archivo_entrada = os.path.join(directorio_entrada, nombre_archivo)

        # Verificar si es un archivo (y no un directorio)
        if os.path.isfile(ruta_archivo_entrada):
            # Leer el contenido del archivo
            with open(ruta_archivo_entrada, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()

            # Procesar el contenido
            contenido_procesado = limpiar_texto(contenido)

            # Crear el nombre del archivo de salida
            nombre_archivo_procesado = os.path.splitext(nombre_archivo)[0] + '_procesado.txt'
            ruta_archivo_salida = os.path.join(directorio_salida, nombre_archivo_procesado)

            # Escribir el contenido procesado en el nuevo archivo
            with open(ruta_archivo_salida, 'w', encoding='utf-8') as archivo_procesado:
                archivo_procesado.write(contenido_procesado)

            print(f"Archivo {nombre_archivo} procesado y guardado como {ruta_archivo_salida}")

# Directorios de entrada y salida
DIRECTORIO_ENTRADA = '/home/'  # Cambia esto por la ruta de tu directorio de entrada
DIRECTORIO_SALIDA = '/home/'    # Cambia esto por la ruta de tu directorio de salida
procesar_archivos_en_directorio(DIRECTORIO_ENTRADA, DIRECTORIO_SALIDA)
