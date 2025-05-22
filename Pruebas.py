from Libraries.NLP_Utils import TukeyNLP

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
bow = nlp.get_bow(docs_tokenizados)

for i in range(len(bow)):
    print("DOC ",i, "\t", bow[i])
    