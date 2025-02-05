"""
Este módulo contiene la función convertir_a_txt, que convierte el texto de un PDF a un 
archivo de texto .txt. Se eliminan los caracteres no deseados del texto extraído,
se filtran las tablas relevantes y se eliminan las líneas similares a las celdas de las tablas.
Se genera un archivo de texto con el texto limpio y las tablas
"""
import pdfplumber
from limpieza import limpiar_caracteres_no_deseados
from texto_duplicado import texto_sin_duplicados
#from ortografia import format_spelling_report
from filtrar_tablas import filtrar_tablas_por_flujograma
from extraer_pagina import extraer_primera_pag
from texto_molesto import filtrar_tabla
from flujograma import filtrar_flujogramas



def convertir_a_txt(pdf, txt):
    """Convierte el texto de un PDF a un archivo de texto .txt."""
    texto_total = "\n--- Página 1 ---\n" + extraer_primera_pag(pdf) + "\n"
    palabras_clave = ["flujograma", "algoritmo", "cavej", "flujogramas"]

    with pdfplumber.open(pdf) as pdf:
        for pagina_num, pagina in enumerate(pdf.pages):
            #if pagina_num >= 12:
            #    break

            print(f"\n--- Procesando Página {pagina_num + 2} ---")

             # Ignorar la primera página
            if pagina_num == 0:
                continue

            margen_izquierdo = 50
            margen_derecho = 50
            margen_superior = 50
            margen_inferior = 0
            area = (margen_izquierdo, margen_superior, pagina.width - margen_derecho, \
                    pagina.height - margen_inferior)
            texto_extraido = pagina.within_bbox(area).extract_text() or ""
            texto_flujogramas = filtrar_flujogramas(texto_extraido, palabras_clave)
            texto_limpio = limpiar_caracteres_no_deseados(texto_flujogramas)
            # Filtrar tablas por flujogramas
            tablas_relevantes = filtrar_tablas_por_flujograma(pagina, texto_limpio)
            # Filtrar tablas irrelevantes
            tablas_relevantes = [tabla for tabla in tablas_relevantes if filtrar_tabla(tabla)]
            tablas_relevantes_filtradas = []
            # recorrer las tablas relevantes y limpiarlas de caracteres no deseados
            for tabla in tablas_relevantes:
                tabla_limpia = [
                    [
                        limpiar_caracteres_no_deseados(str(celda)) if celda else ""
                        for celda in fila
                    ]
                    for fila in tabla
                ]
                tablas_relevantes_filtradas.append(tabla_limpia)
            # Eliminar duplicados de texto
            texto_filtrado = texto_sin_duplicados(texto_limpio, tablas_relevantes)
            #texto_filtrado = texto_sin_duplicados(texto_filtrado, flujogramas)
            #texto_final, correcciones = revisar_ortografia(texto_filtrado)

            texto_total += f"\n--- Página {pagina_num + 1} ---\n"
            texto_total += texto_filtrado + "\n"

            # Agregar tablas relevantes
            for idx, tabla in enumerate(tablas_relevantes_filtradas):
                texto_total += f"Tabla {idx + 1}:\n"
                for fila in tabla:
                    texto_total += "\t".join(str(celda) if celda else "" for celda in fila) + "\n"

    # Imprimir reporte de correcciones
    #print("\n" + format_spelling_report(correcciones))

    with open(txt, "w", encoding="utf-8") as archivo_txt:
        archivo_txt.write(texto_total)
    print(f"El archivo TXT ha sido generado: {txt}")
    