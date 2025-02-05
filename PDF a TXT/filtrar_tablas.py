"""
se filtran las tablas relevantes y se eliminan las líneas similares a las celdas de las tablas.
"""

# calcular distancia sirve para calcular la distancia entre dos cuadros delimitadores
def calcular_distancia(bbox1, bbox2):
    """Calcula la distancia entre dos cuadros delimitadores (bounding boxes)."""
    x_dist = max(0, max(bbox1[0], bbox2[0]) - min(bbox1[2], bbox2[2]))
    y_dist = max(0, max(bbox1[1], bbox2[1]) - min(bbox1[3], bbox2[3]))
    return x_dist + y_dist

# filtrar_tablas_por_flujograma sirve para filtrar tablas para evitar cuadros de flujogramas y texto general
def filtrar_tablas_por_flujograma(pagina, texto,  umbral_distancia=25, min_filas=2, min_columnas=2):
    """
    Filtra tablas para evitar cuadros de flujogramas y texto general.
    """

    if not texto.strip():
        return "", ""
    
    tablas = pagina.extract_tables() or []
    cuadros_descartados = []
    tablas_relevantes = []
    eliminados = []

    # Extraer cuadros (bounding boxes) de las tablas
    cuadros = pagina.find_tables()

    # Funciones auxiliares
    # calcular_proporcion_texto sirve para calcular la proporción de celdas que contienen texto vs. celdas vacías.
    def calcular_proporcion_texto(tabla):
        """Calcula la proporción de celdas que contienen texto vs. celdas vacías."""
        celdas_total = 0
        celdas_con_texto = 0
        for fila in tabla:
            for celda in fila:
                if celda and isinstance(celda, str):
                    celdas_total += 1
                    if celda.strip():
                        celdas_con_texto += 1
        return celdas_con_texto / celdas_total if celdas_total > 0 else 0

    # verificar si la tabla tiene una estructura regular (mismo número de columnas).
    def es_estructura_regular(tabla):
        """Verifica si la tabla tiene una estructura regular (mismo número de columnas)."""
        if not tabla:
            return False
        num_columnas = len(tabla[0])
        return all(len(fila) == num_columnas for fila in tabla)

    # verificar si el cuadro tiene dimensiones razonables para una tabla.
    def tiene_bordes_definidos(bbox):
        """Verifica si el cuadro tiene dimensiones razonables para una tabla."""
        ancho = bbox[2] - bbox[0]
        alto = bbox[3] - bbox[1]
        area = ancho * alto
        proporcion = max(ancho/alto, alto/ancho)

        # Criterios más estrictos para evitar detectar texto normal
        return (proporcion < 5 and area > 400) or area > 1000

    # verificar si el elemento tiene características típicas de un elemento de flujograma.
    def es_elemento_flujograma(tabla, bbox):
        if not tabla:
            return False

        # Obtener texto completo
        texto = ' '.join([' '.join(str(celda) for celda in fila if celda) \
                        for fila in tabla]).lower()

        # Criterios específicos de flujograma
        es_compacto = len(tabla) == 1 or (len(tabla) == 2 and len(tabla[0]) <= 2)
        texto_corto = len(texto.split()) < 20

        ancho = bbox[2] - bbox[0]
        alto = bbox[3] - bbox[1]
        proporcion = max(ancho/alto, alto/ancho)
        forma_cuadrada = 0.7 < proporcion < 1.5

        # Debe cumplir al menos dos criterios para ser considerado flujograma
        return (es_compacto) and (texto_corto or forma_cuadrada)

    # verificar si la estructura parece ser una tabla válida.
    def es_tabla_valida(tabla):
        if not tabla or not tabla[0]:
            return False

        # Contar celdas con contenido significativo por columna
        contenido_por_columna = []
        num_columnas = len(tabla[0])

        for col in range(num_columnas):
            celdas_con_contenido = sum(
                1 for fila in tabla 
                if col < len(fila) and fila[col] and str(fila[col]).strip()
            )
            contenido_por_columna.append(celdas_con_contenido)

        # Una tabla válida debe tener al menos dos columnas con contenido
        columnas_con_contenido = sum(1 for cont in contenido_por_columna if cont > 0)

        # Verificar si tiene estructura de tabla
        tiene_estructura = (
            columnas_con_contenido >= 2 and  # Al menos dos columnas con contenido
            # Al menos una columna con múltiples valores
            any(cont >= 2 for cont in contenido_por_columna)
        )

        # Verificar si hay patrones de tabla
        tiene_patrones_tabla = any([
            # Buscar numeración
            any(str(celda).strip().startswith(str(idx+1) + '.') for idx, fila \
                 in enumerate(tabla) for celda in fila if celda),
            # Buscar encabezados con dos puntos
            any(isinstance(celda, str) and ':' in celda for fila in tabla[:1] for celda in fila),
            # Buscar estructura de datos consistente
            all(any(str(celda).strip() for celda in fila) for fila in tabla)
        ])

        return tiene_estructura or tiene_patrones_tabla

    def es_bloque_texto(tabla):
        """Detecta si el elemento parece ser un bloque de texto continuo."""
        if not tabla:
            return False

        # Contar celdas con texto significativo
        celdas_con_texto = sum(
            1 for fila in tabla
            for celda in fila
            if celda and isinstance(celda, str) and len(str(celda).strip()) > 0
        )

        # Otros cálculos relacionados con 'celdas_con_texto' y 'palabras'
        if celdas_con_texto == 0:
        # Retorna False o el valor adecuado según la lógica del programa
            return False

        # Obtener texto total
        texto_total = ' '.join(
            str(celda).strip()
            for fila in tabla
            for celda in fila
            if celda and isinstance(celda, str)
        )

        palabras = texto_total.split()

        # Criterios más estrictos para bloques de texto
        return (
            (celdas_con_texto == 1 and len(palabras) > 30) or  # Una sola celda con mucho texto
            (len(tabla) == 1 and len(tabla[0]) == 1) or  # Una única celda
            # Promedio alto de palabras por celda
            (celdas_con_texto <= 2 and len(palabras) / celdas_con_texto > 25)
        )

    for idx, tabla in enumerate(tablas):
        if idx >= len(cuadros):
            continue

        bbox_tabla = cuadros[idx].bbox
        filas = len(tabla)
        columnas = max(len(fila) for fila in tabla if fila)

        # Primero verificar si es un flujograma
        if es_elemento_flujograma(tabla, bbox_tabla):
            cuadros_descartados.append(bbox_tabla)
            eliminados.append(tabla)
            print(f"flujogramas palabras: {eliminados}")
            continue

        # Verificar si es un bloque de texto
        if es_bloque_texto(tabla):
            cuadros_descartados.append(bbox_tabla)
            continue

        # Verificar si es una tabla válida
        if es_tabla_valida(tabla) and es_estructura_regular(tabla):
            tablas_relevantes.append(tabla)
            continue

        # Criterios adicionales solo si no cumple los anteriores
        if any([
            filas < min_filas or columnas < min_columnas,
            calcular_proporcion_texto(tabla) < 0.2,
            not tiene_bordes_definidos(bbox_tabla),
        ]):
            cuadros_descartados.append(bbox_tabla)
            continue

        # Verificar proximidad a elementos descartados
        es_cercano_a_descartado = False
        for bbox_otra in cuadros_descartados:
            distancia = calcular_distancia(bbox_tabla, bbox_otra)
            if distancia < umbral_distancia:
                es_cercano_a_descartado = True
                break

        if es_cercano_a_descartado:
            cuadros_descartados.append(bbox_tabla)
        else:
            tablas_relevantes.append(tabla)

    return tablas_relevantes
