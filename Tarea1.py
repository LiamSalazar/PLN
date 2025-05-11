import os

def leerDocumentos(carpeta):
    contenido_total = ""
    for nombre_archivo in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        if os.path.isfile(ruta_completa):
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                contenido_total += archivo.read()  
    return contenido_total

def eliminar_stopwords(texto, stop_words):
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words]
    return palabras_filtradas

def eliminar_caracteres_especiales(texto, caracteres):
    for caracter in caracteres:
        texto = texto.replace(caracter, '')
    return texto


carpeta = "./ArchivosTarea"  
texto_normalizado = []
stop_words = [
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se',
    'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al',
    'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o',
    'sí', 'porque', 'muy', 'sin', 'también', 'me', 'hasta',
    'donde', 'todo', 'nos', 'uno', 'ni', 'yo', 'tú', 'él',
    'ella', 'nosotros', 'ellos', 'ellas', 'mi', 'tu', 'te',
    'me', 'sí', 'nos', 'ese', 'esa', 'esto', 'eso'
]
caracteres = [',', '.', '!', '?', '¿', '¡', ':', ';', '-', '_', '(', ')', '[', ']', '{', '}', "'", '"']

texto = leerDocumentos(carpeta)
texto = texto.lower() 
texto = eliminar_caracteres_especiales(texto, caracteres)
texto_normalizado = eliminar_stopwords(texto, stop_words)
print(texto_normalizado)