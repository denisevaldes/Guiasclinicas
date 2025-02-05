import re
from spellchecker import SpellChecker

def revisar_ortografia(text, custom_words=None):
    """
    Revisa y corrige la ortografía de un texto en español e inglés, permitiendo
    excepciones para términos especiales.
    """
    # Inicializar correctores en ambos idiomas
    spell_es = SpellChecker(language='es')
    # Agregar palabras personalizadas si se proporcionan
    if custom_words:
        spell_es.word_frequency.load_words(custom_words)
    # Procesar el texto línea por línea para mantener el formato
    lines = text.splitlines()
    corrections = {}
    corrected_lines = []

    for line in lines:
        words = re.findall(r'\b\w+\b', line)  # Extraer palabras de la línea actual
        corrected_line = line  # Línea corregida que se irá actualizando
        for word in words:
            # Ignorar palabras que son números o están en la lista de términos especiales
            if word.isdigit() or (custom_words and word.lower() in custom_words):
                continue
            # Revisar en español primero
            if word.lower() not in spell_es:
                # Obtener la mejor sugerencia
                suggestion_es = spell_es.correction(word.lower())
                if suggestion_es and suggestion_es != word.lower():
                    corrected_word = suggestion_es.capitalize() if \
                    word[0].isupper() else suggestion_es
                    corrections[word] = corrected_word
                    # Reemplazar palabra en la línea
                    corrected_line = re.sub(rf'\b{word}\b', corrected_word,\
                                            corrected_line)
        corrected_lines.append(corrected_line)

    # Reconstruir el texto respetando los saltos de línea
    corrected_text = "\n".join(corrected_lines)
    return corrected_text, corrections

def format_spelling_report(corrections):
    """
    Formatea los errores de ortografía en un reporte legible.
    """
    if not corrections:
        return "No se encontraron errores ortográficos."
    report = ["Errores corregidos:"]
    for original, corrected in corrections.items():
        report.append(f"'{original}' fue corregido a '{corrected}'")
    return "\n".join(report)
