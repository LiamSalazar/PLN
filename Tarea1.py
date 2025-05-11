import os

stop_words = [
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se',
    'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al',
    'lo', 'como', 'mas', 'pero', 'sus', 'le', 'ya', 'o',
    'porque', 'muy', 'sin', 'también', 'hasta',
    'donde', 'todo', 'nos', 'uno', 'ni', 'yo', 'tú', 'él',
    'ella', 'nosotros', 'ellos', 'ellas', 'mi', 'tu', 'te',
    'me', 'si', 'nos', 'ese', 'esa', 'esto', 'eso', 'es', 'son', 'he', 'has', 'han', 'había'
]
caracteres = [',', '.', '!', '?', '¿', '¡', ':', ';', '-', '_', '(', ')', '[', ']', '{', '}', "'", '"']

def leerDocumentos(carpeta):
    contenido_total = ""
    for nombre_archivo in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        if os.path.isfile(ruta_completa):
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                contenido_total += archivo.read()  
    return contenido_total

def eliminar_stopwords(texto):
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words]
    return palabras_filtradas

def eliminar_caracteres_especiales(texto):
    for caracter in caracteres:
        texto = texto.replace(caracter, '')
    return texto

def eliminar_acentos(texto):
    acentos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
    }
    for acento, sin_acento in acentos.items():
        texto = texto.replace(acento, sin_acento)
    return texto

def normalizar_texto(texto):
    texto = texto.lower()  
    texto = eliminar_caracteres_especiales(texto) 
    texto = eliminar_acentos(texto) 
    texto_normalizado = eliminar_stopwords(texto) 
    return texto_normalizado

def crearDiccionario(texto_normalizado):
    diccionario = {}
    for palabra in texto_normalizado:
        if palabra in diccionario:
            diccionario[palabra] += 1
        else:
            diccionario[palabra] = 1
    return diccionario

def palabras_mas_frecuentes(diccionario, n):
    palabras_ordenadas = sorted(diccionario.items(), key=lambda palabra_total: palabra_total[1], reverse=True)
    return palabras_ordenadas[:n]

carpeta = "./ArchivosTarea"

texto = leerDocumentos(carpeta)
texto_normalizado = normalizar_texto(texto)
print("Palabras más frecuentes:")
diccionario = crearDiccionario(texto_normalizado)
palabras_frecuentes = palabras_mas_frecuentes(diccionario, 50)

for palabra, frecuencia in palabras_frecuentes:
    print(f"{palabra}: {frecuencia}")
