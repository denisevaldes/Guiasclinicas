"""
Convierte la primera página de un PDF a imagen y extrae el texto con OCR.
"""
from pdf2image import convert_from_path
from PIL import ImageFilter
from limpieza import limpiar_caracteres_no_deseados
#from ortografia import revisar_ortografia, format_spelling_report
import pytesseract

def extraer_primera_pag (path):
    # Convertir solo la primera página del PDF a imagen
    imagenes = convert_from_path(path, first_page=1, last_page=1, dpi=700)

    if len(imagenes) > 1:
        imagen = imagenes[1]
    else:
        imagen = imagenes[0]

    # Convertir la imagen a escala de grises
    #imagen = imagenes[0].convert('L')

    # Aplicar binarización para mejorar el contraste
    imagen = imagen.convert('L').point(lambda x: 0 if x < 220 else 290, '1')

    imagen = imagen.filter(ImageFilter.MedianFilter())

    # Usar OCR para extraer el texto
    texto_pagina_1 = pytesseract.image_to_string(imagen)
    texto_pagina = limpiar_caracteres_no_deseados(texto_pagina_1)
    limpio = texto_pagina.splitlines()

    # Eliminamos líneas vacías consecutivas manteniendo solo una
    filtered_lines = []
    prev_empty = False
    
    for line in limpio:
        is_empty = not line.strip()
        if not (is_empty and prev_empty):
            filtered_lines.append(line)
        prev_empty = is_empty
    
    # Volver a unir el texto
    result = '\n'.join(filtered_lines)
    #result, correcciones = revisar_ortografia(result)

    # Imprimir reporte de correcciones
    #print("\n" + format_spelling_report(correcciones))

    return result
