import os

class TukeyNLP:
    def __init__(self):
        self.stop_words = [
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se',
            'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al',
            'lo', 'como', 'mas', 'pero', 'sus', 'le', 'ya', 'o',
            'porque', 'muy', 'sin', 'también', 'hasta',
            'donde', 'todo', 'nos', 'uno', 'ni', 'yo', 'tú', 'él',
            'ella', 'nosotros', 'ellos', 'ellas', 'mi', 'tu', 'te',
            'me', 'si', 'ese', 'esa', 'esto', 'eso', 'es', 'son', 'he', 'has', 'han', 'había',
            'este', 'esta', 'estos', 'estas'
        ]
        self.caracteres = [',', '.', '!', '?', '¿', '¡', ':', ';', '-', '_', '(', ')', '[', ']', '{', '}', "'", '"']

    def leer_archivos(self, carpeta):
        documentos = []
        for nombre_archivo in os.listdir(carpeta):
            ruta_completa = os.path.join(carpeta, nombre_archivo)
            if os.path.isfile(ruta_completa):
                with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read().strip()
                    if contenido:
                        documentos.append(contenido)
        return documentos

    def eliminar_caracteres_especiales(self, texto):
        for caracter in self.caracteres:
            texto = texto.replace(caracter, ' ')
        return texto

    def eliminar_acentos(self, texto):
        acentos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
        for acento, sin_acento in acentos.items():
            texto = texto.replace(acento, sin_acento)
        return texto

    def tokenize(self, texto):
        tokens = []
        palabra = ''
        for char in texto:
            if char != ' ':
                palabra += char
            else:
                if palabra:
                    tokens.append(palabra)
                    palabra = ''
        if palabra:
            tokens.append(palabra)
        return tokens

    def eliminar_stopwords(self, tokens):
        return [palabra for palabra in tokens if palabra not in self.stop_words]

    def normalizar_documento(self, documento):
        documento = documento.lower()
        documento = self.eliminar_caracteres_especiales(documento)
        documento = self.eliminar_acentos(documento)
        tokens = self.tokenize(documento)
        tokens = self.eliminar_stopwords(tokens)
        return tokens

    def normalizar_documentos(self, lista_documentos):
        return [self.normalizar_documento(doc) for doc in lista_documentos]

    def get_vocabulary(self, lista_documentos):
        vocabulario = set()
        for doc in lista_documentos:
            vocabulario.update(doc)
        return list(vocabulario)
    
    def bag_of_words(self, vocabulario, tokens):
        vector = [0] * len(vocabulario)
        for word in tokens:
            if word in vocabulario:
                idx = vocabulario.index(word)
                vector[idx] += 1
        return vector

nlp = TukeyNLP()
# Pruebas
docs = ["Hola me llamo Liam", "El perro come pescado", "El gato come pescado"]
print("\nPrueba 1:")
print("\nDocumentos tokenizados:")
docs_tokenizados = nlp.normalizar_documentos(docs)
print(docs_tokenizados)
print("\nVocabulario:")
vocabulario = nlp.get_vocabulary(docs_tokenizados)
print(vocabulario)
print("\nBag of words:")
bow = []
for doc in docs_tokenizados:
    aux = nlp.bag_of_words(vocabulario, doc)
    bow.append(aux)

for i in range(len(bow)):
    print("DOC ",i, "\t", bow[i])
    