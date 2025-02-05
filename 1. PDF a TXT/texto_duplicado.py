"""
Se eliminan las líneas de un texto que son similares a las celdas de las tablas
encontradas en un documento PDF. Se utiliza la función `similitud_texto` para
determinar si dos textos son similares, y se eliminan las líneas que cumplen
con este criterio.
"""
import re
from difflib import SequenceMatcher

def normalizar_texto(texto):
    """Normaliza el texto eliminando caracteres especiales y espacios."""
    texto = re.sub(r'[\n\r\t,]+', ' ', texto)  # Reemplazar saltos de línea, comas y tabulaciones
    texto = re.sub(r'\s+', ' ', texto)  # Normalizar espacios
    texto = texto.lower().strip() # Convertir a minúsculas y eliminar espacios al inicio y final
    return texto

def similitud_texto(texto1, texto2, umbral=0.8):
    """Compara dos textos y determina si son similares basado en un umbral."""
    texto1 = normalizar_texto(texto1)
    texto2 = normalizar_texto(texto2)

    # Si uno de los textos está completamente contenido en el otro
    if texto1 in texto2 or texto2 in texto1:
        return True

    # Usar SequenceMatcher para comparaciones más flexibles
    ratio = SequenceMatcher(None, texto1, texto2).ratio() # Ratio de similitud
    return ratio > umbral # Determinar si la similitud es mayor al umbral

def extraer_contenido_tabla(tabla):
    """Extrae todo el contenido significativo de una tabla."""
    contenido = set()

    for fila in tabla:
        # Procesar cada celda no vacía
        texto_fila = ' '.join(str(celda) for celda in fila if celda and str(celda).strip())
        if texto_fila:
            # Dividir por saltos de línea en caso de que haya múltiples líneas en una celda
            for linea in texto_fila.split('\n'):
                if linea.strip():
                    contenido.add(normalizar_texto(linea))

            # También agregar la línea completa
            contenido.add(normalizar_texto(texto_fila))

    return contenido

def texto_sin_duplicados(texto, tablas):
    """Elimina líneas del texto que aparecen en las tablas."""
    texto_lineas = [linea.strip() for linea in texto.split('\n') if linea.strip()]
    contenido_tablas = set()

    # Extraer todo el contenido de las tablas
    for tabla in tablas:
        contenido_tablas.update(extraer_contenido_tabla(tabla))

    texto_limpio = []
    for linea in texto_lineas:
        es_duplicado = False # Indica si la línea es similar a contenido de tabla
        linea_norm = normalizar_texto(linea)

        # Verificar si la línea es similar a algún contenido de las tablas
        for contenido in contenido_tablas:
            if similitud_texto(linea_norm, contenido):
                #print(f"contenido: {contenido}")
                #print(f"Eliminada (similar a contenido de tabla): {linea}")
                es_duplicado = True
                break

        if not es_duplicado:
            texto_limpio.append(linea)

    return '\n'.join(texto_limpio)
