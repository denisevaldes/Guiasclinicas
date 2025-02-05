"""
Código para limpiar texto de caracteres no deseados
"""
import re
import unicodedata

def limpiar_caracteres_no_deseados(texto):
    """
    Limpieza de texto que preserva formato y saltos de línea.
    """
    try:
        # Paso 1: Normalizar la codificación Unicode
        texto = unicodedata.normalize('NFKD', texto)

        # Paso 2: Eliminar caracteres de control excepto saltos de línea
        texto = ''.join(char for char in texto 
                       if char == '\n' or unicodedata.category(char)[0] != 'C')

        # Paso 3: Eliminar específicamente los caracteres problemáticos
        caracteres_problematicos = [
            '\uFFFD',  # Carácter de reemplazo Unicode
            '\u25A0',  # Cuadrado negro
            '\u25A1',  # Cuadrado blanco
            '\u2022',  # Bullet point
            '�',       # Signo de interrogación en cuadro
        ]

        for char in caracteres_problematicos:
            texto = texto.replace(char, '')

        # Paso 4: Eliminar caracteres no deseados pero mantener español y saltos de línea
        # Nota: \n incluido en la lista de caracteres permitidos
        texto = re.sub(r'\uf0fe', 'X', texto)  # Usando la expresión regular para reemplazar
        texto = re.sub(r'[^\w\s\náéíóúÁÉÍÓÚñÑüÜX%¿¡.,;:()/<>{}[\]=-?!]', '', texto)

        # Paso 5: Eliminar espacios múltiples en cada línea pero preservar saltos de línea
        lineas = texto.split('\n')
        lineas_limpias = [re.sub(r'\s+', ' ', linea).strip() for linea in lineas]
        texto = '\n'.join(lineas_limpias)

        # Paso 6: Eliminar líneas vacías múltiples
        texto = re.sub(r'\n\s*\n', '\n', texto)

        return texto

    except (TypeError, ValueError, re.error) as e:
        print(f"Error al limpiar el texto: {str(e)}")
        return texto
