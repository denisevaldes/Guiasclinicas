"""
Función encargada de filtrar páginas completas de flujogramas.
"""

def filtrar_flujogramas(texto, palabras_clave):
    """Filtrar el texto si contiene alguna de las palabras clave en las dos
    primeras palabras de la primera línea."""
    if not texto:
        return ""

    # Extraer la primera línea
    primera_linea = texto.split('\n', 1)[0].lower()
    # Tomar solo las dos primeras palabras
    primeras_dos_palabras = ' '.join(primera_linea.split()[:2])

    contiene_palabras_clave = any(palabra_clave.lower() in primeras_dos_palabras
                                  for palabra_clave in palabras_clave)

    return texto if not contiene_palabras_clave else ""
