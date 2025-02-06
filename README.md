# 🏥 Conversión de Guías Clínicas 
Este proyecto proporciona herramientas para convertir guías clínicas de formato PDF a .txt y de .txt a JSON. El proceso extrae texto y tablas, excluyendo imágenes y gráficos, para facilitar el análisis de datos clínicos.

## Requisitos previos 
- Python 3.9.21
- Bibliotecas:
  -  pdfplumber
  -  pdf2image
  -  PIL
  -  pytesseract
  -  google.generativeai

## 📌 Uso

### 🚀 Conversión de PDF a TXT

Para convertir una guía clínica en formato PDF a texto, sigue estos pasos:

1. **Accede al directorio del proyecto**  
   Asegúrate de estar en la carpeta principal del proyecto, donde se encuentra el archivo `main.py`.

2. **Configura las rutas de entrada y salida**  
   Abre `main.py` y edita las siguientes variables con las rutas correctas del archivo PDF de entrada y la ubicación donde deseas guardar el archivo de texto:

   ```python
   RUTA_PDF = r"ruta/a/tu/archivo.pdf"
   RUTA_TXT = "ruta/donde/guardar/archivo.txt"

3. **Ejecuta el script**
   Una vez configuradas las rutas, ejecuta el script desde tu entorno de desarrollo o usando Python en la terminal

### Limpieza de Archivos TXT

Después de convertir las guías clínicas de PDF a TXT, el siguiente paso es limpiar los archivos de texto. Esta etapa se realiza utilizando varios scripts que se encuentran en la segunda carpeta del proyecto. Cada script debe ejecutarse por separado, proporcionando las rutas de entrada y salida necesarias.

#### Pasos para la Limpieza:

1. **Navega a la carpeta de limpieza**: Asegúrate de estar en el directorio donde se encuentran los scripts de limpieza.

2. **Ejecuta los scripts de limpieza**: Cada script en esta carpeta realiza una tarea específica de limpieza.

#### notas adicionales

- **Limitaciones del Corrector Ortográfico**: 
  El script encargado de la corrección ortográfica fue diseñado específicamente para los primeros archivos procesados, utilizando un diccionario personalizado. Como resultado, es posible que no corrija todas las faltas de ortografía en archivos nuevos o diferentes. Se recomienda revisar manualmente los archivos después de la corrección para asegurar la precisión ortográfica.
