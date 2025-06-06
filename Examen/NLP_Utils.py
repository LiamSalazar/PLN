import math
import os
from nltk.corpus import stopwords

import numpy as np

class TukeyNLP:
    def __init__(self, stopwords_extra=None):
        self.caracteres = [',', '.', '!', '?', '¿', '¡', ':', ';', '-', '_', '(', ')', '[', ']', '{', '}', "'", '"']
        base_stopwords = stopwords.words("english")
        self.stop_words = set(w.lower() for w in base_stopwords)
        if stopwords_extra:
            self.stop_words.update(w.lower() for w in stopwords_extra)

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

    def normalizar_documento(self, documento):
        documento = documento.lower()
        documento = self.eliminar_caracteres_especiales(documento)
        documento = self.eliminar_acentos(documento)
        tokens = self.tokenize(documento)
        tokens = [palabra for palabra in tokens if palabra not in self.stop_words]
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

    def get_bow(self, lista_documentos):
        vocabulario = self.get_vocabulary(lista_documentos)
        bow = []
        for doc in lista_documentos:
            aux = self.bag_of_words(vocabulario, doc)
            bow.append(aux)
        return vocabulario, bow
    
    def tf_idf(self, tokens, vocab):
        no_docs = len(tokens)
        # IDF
        idf = dict()
        for word in vocab:
            n_t = sum(1 for document in tokens if word in document)
            idf[word] = math.log(no_docs/(1+n_t))
        # TF-IDF
        tf_idf_matrix = []
        for doc in tokens:
            doc_len = len(doc)
            tf_idf_vector = []
            for word in vocab:
                tf = doc.count(word) / doc_len
                tf_idf_val = tf * idf[word]
                tf_idf_vector.append(tf_idf_val) 
            tf_idf_matrix.append(tf_idf_vector)
        return np.array(tf_idf_matrix)