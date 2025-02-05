"""
script para analizar múltiples archivos de texto usando Gemini API para encontrar elementos comunes.
"""
from pathlib import Path
import google.generativeai as genai
#import os

def analyze_text_files(api_key, directory_path):
    """
    Analiza múltiples archivos de texto usando Gemini API para encontrar elementos comunes.
    
    Args:
        api_key (str): Tu API key de Google
        directory_path (str): Ruta al directorio con los archivos .txt
    """
    # Configurar la API de Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Leer todos los archivos .txt del directorio
    text_contents = []
    file_names = []

    for file_path in Path(directory_path).glob('*.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text_contents.append(file.read())
            file_names.append(file_path.name)

    if not text_contents:
        print("No se encontraron archivos .txt en el directorio especificado.")
        return

    # Crear el prompt para Gemini
    prompt = f"""
    analiza los 19 textos. 
    Analiza los siguientes indices y encuentra los elementos comunes en la mayoria de ellos.
    Proporciona un índice de temas o elementos que aparecen en la mayoria de los textos.
    Toma en cuenta solo los temas que esten enumerados.
    Dime también en cuantos de los textos se encuentra cada tema que me des.
    Textos a analizar:
    {'-' * 50}
    """ + "\n\n".join(f"Archivo: {name}\nContenido:\n{content}\n{'-' * 50}" 
                      for name, content in zip(file_names, text_contents))

    try:
        # Obtener respuesta de Gemini
        response = model.generate_content(prompt)
        # Guardar la respuesta en un archivo
        output_path = Path(directory_path) / "indice_en_comun.txt"
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write("Análisis de elementos comunes:\n")
            output_file.write(response.text)
        print("\nAnálisis de elementos comunes:")
        print(response.text)

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")

    # Obtén el recuento de tokens
    token_count = model.count_tokens(prompt)

    print(f"Total de tokens: {token_count}")

# Ejemplo de uso
if __name__ == "__main__":
    API_KEY = "clave"  # Reemplaza con tu API key
    DIRECTORY = "/home/"   # Reemplaza con la ruta a tu directorio

    analyze_text_files(API_KEY, DIRECTORY)
