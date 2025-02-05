"""
script que reemplaza puntos por comas en un archivo de texto.
"""
import re

def reemplazar_puntos_por_comas(texto):
    """
    Reemplaza cualquier número seguido de un punto por el mismo número seguido de una coma.
    """
    # Expresión regular para encontrar números seguidos de un punto
    patron = re.compile(r"(\d+)\.")

    # Reemplazar todos los números seguidos de un punto por el número seguido de una coma
    texto_procesado = patron.sub(r"\1,", texto)

    return texto_procesado

def procesar_archivo(archivo_entrada, archivo_salida):
    """
    Procesa un archivo de texto, reemplaza puntos por espacios en líneas que 
    comienzan con un número y un punto, y guarda el resultado en un archivo de salida.
    """
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r', encoding='utf-8') as file:
        texto = file.read()

    #convertir todo el texto a minúsculas
    texto = texto.lower()
    # Procesar el texto
    texto_procesado = reemplazar_puntos_por_comas(texto)

    # Escribir el resultado en el archivo de salida
    with open(archivo_salida, 'w', encoding='utf-8') as file:
        file.write(texto_procesado)


def main():
    # Rutas de archivo de entrada y salida
    archivo_entrada = "/home/"  # Cambia esto por la ruta de tu archivo de entrada
    archivo_salida = "/home/"    # Cambia esto por la ruta de tu archivo de salida

    # Procesar el archivo
    procesar_archivo(archivo_entrada, archivo_salida)
    print(f"Procesamiento completado. Resultado guardado en: {archivo_salida}")

if __name__ == "__main__":
    main()
