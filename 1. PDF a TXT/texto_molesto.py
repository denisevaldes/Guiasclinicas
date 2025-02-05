"""
Se filtra texto que se encuentra en los pie de página de los lados de las paginas, 
que en caso de no ser filtrado es mostrado como tabla. 
"""
import re

def filtrar_texto(texto):
    """Determina si un texto es molesto basándose en palabras clave o patrones."""
    palabras_clave = [r"\boiretsiniM\b", r"\bdulaS\b", r"\bgpc\b", \
                      r"\bGPC\b", r"\bCPG\b", r"\bLASNIM\b"]
    patron = re.compile("|".join(palabras_clave), re.IGNORECASE)
    return bool(patron.search(texto))

def filtrar_tabla(tabla):
    """Filtra tablas irrelevantes basándose en contenido."""
    for fila in tabla:
        for celda in fila:
            if celda and filtrar_texto(celda):
                return False  # Descarta la tabla si contiene texto molesto
    return True  # Acepta la tabla si no tiene texto molesto