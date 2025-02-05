"""
Procesamiento de guías clínicas en formato de texto plano para extraer secciones
y subsecciones definidas en un archivo JSON.
"""
import re
import os
import json

def identificar_secciones_definidas(texto, secciones_interes):
    """
    Se identifican las secciones y subsecciones definidas en el texto de la guía clínica.
    """
    # Expresión para identificar títulos de secciones con numeración
    patron = re.compile(
        r'^(?!.*(?:Página|Fig\.|Tabla))'  # Evitar líneas que contengan "Página", "Fig." o "Tabla"
        r'(\d{1,2}(\.\d{1,2})*)\.\s*'     # Capturar numeración (ej. "1", "1.1", "1.1.1")
        r'([^\n]+)',                      # Capturar el título
        re.MULTILINE
    )

    # Lista para almacenar las secciones encontradas
    secciones_encontradas = []

    # Stack para rastrear las secciones activas
    stack = []

    # Buscar todas las coincidencias en el texto
    coincidencias = list(patron.finditer(texto))

    for i, match in enumerate(coincidencias):
        # Extraer la numeración y el título
        numeracion = match.group(1)  # Numeración completa (ej. "1.1.1")
        titulo = match.group(3).strip()  # Título de la sección

        # Validar que la numeración no sea None y que no tenga más de 2 dígitos en ninguna parte
        if numeracion is None or any(len(part) > 2 for part in numeracion.split('.')):
            # Omitir esta línea si no hay numeración o si tiene más de 2 dígitos en alguna parte
            continue

        # Calcular el nivel de anidación
        nivel = len(numeracion.split('.'))  # Nivel de anidación
    
        # Índice de inicio y fin
        inicio = match.start()

        # Calcular el fin en función de la jerarquía
        fin = len(texto)  # Por defecto, el fin es el final del texto
        for j in range(i + 1, len(coincidencias)):
            siguiente_numeracion = coincidencias[j].group(1)
            siguiente_nivel = len(siguiente_numeracion.split('.'))
            if nivel == 1 and siguiente_nivel >= 1:
                fin = coincidencias[j].start() - 1
                break
            if nivel == 2 and (siguiente_nivel == 1 or siguiente_nivel >= 2):
                fin = coincidencias[j].start() - 1
                break
            if nivel == 3 and siguiente_nivel <= 3:
                fin = coincidencias[j].start() - 1
                break
            if nivel == 4 and siguiente_nivel <= 4:
                fin = coincidencias[j].start() - 1
                break

        # Extraer el contenido de la sección
        contenido = texto[inicio:fin].strip()

        # Filtrar el contenido para eliminar líneas no válidas
        lineas_validas = []
        for linea in contenido.split('\n'):
            if re.match(r'^\d{1,2}\.$', linea.strip()) and not re.match(r'^\d{1,2}(\.\d{1,2})+\.$', linea.strip()):
                continue
            lineas_validas.append(linea)
        contenido = '\n'.join(lineas_validas).strip()

        # Crear la estructura de la sección
        seccion_actual = {
            "id": titulo.lower().replace(" ", "_"),
            "titulo": titulo,
            "numeracion": numeracion,
            "contenido": contenido,
            "subsecciones": []
        }

        # Verificar si el título es una sección de interés
        if titulo.lower() in [s.lower() for s in secciones_interes]:
            # Es una sección de interés, agregarla a la lista principal
            secciones_encontradas.append(seccion_actual)
            # Actualizar el stack
            stack = [seccion_actual]
        elif stack:
            print(f"Comparando {numeracion} con {stack[-1]['numeracion']}")
            # Es una subsección o subsubsección, encontrar la sección padre correcta
            while stack and not numeracion.startswith(stack[-1]["numeracion"] + "."):
                print(f"Removiendo {stack[-1]['numeracion']} del stack")
                stack.pop()  # Remover secciones que no son padre
            if stack:
                # Agregar la subsección o subsubsección a la sección padre
                stack[-1]["subsecciones"].append(seccion_actual)
                # Actualizar el stack
                stack.append(seccion_actual)

    return secciones_encontradas

def procesar_archivo(archivo_entrada, secciones_interes):
    """
    Procesa un archivo de texto e identifica las secciones.
    """
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r', encoding='utf-8') as file:
        texto = file.read()

    # Identificar las secciones
    secciones = identificar_secciones_definidas(texto, secciones_interes)

    return secciones

def main():
    # Definir las secciones de interés
    secciones_interes = ["introducción", "objetivos", "recomendaciones", "implementación de la guía", "desarrollo de la guía", "alcance de la guía", "descripción y epidemiología del problema", "recomendaciones de la guía", "epidemiología"]

    # Directorio de entrada y archivo de salida JSON
    archivo_entrada = "/home/denise/prueba/AAAjson/textoslistosparajson/diabetes2_2015.txt"
    archivo_salida_json = "/home/denise/prueba/AAAjson/textoslistosparajson/textos_sin_juntar/diabetes22.json"

    # Crear el directorio de salida si no existe
    os.makedirs(os.path.dirname(archivo_salida_json), exist_ok=True)

    # Procesar todos los archivos .txt en el directorio de entrada
    resultados = []

    secciones = procesar_archivo(archivo_entrada, secciones_interes)
    resultados.extend(secciones)


    # Guardar los resultados en un archivo JSON
    with open(archivo_salida_json, 'w', encoding='utf-8') as json_file:
        json.dump(resultados, json_file, indent=4, ensure_ascii=False)

    print(f"Resultados guardados en: {archivo_salida_json}")

if __name__ == "__main__":
    main()
