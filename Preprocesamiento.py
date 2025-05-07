# Oración a procesar
oracion = "El perro,,, com!!!e croquetas???"

stopwords = ["el","la","o","y","que"]
caracteres =  [',','.','!','?','¿']

oracion = oracion.lower() # Eliminar mayúsculas

# ELiminar los caracteres especiales
oracion = ''.join([c for c in oracion if c not in caracteres])

vector_oracion = oracion.split() # Separar en un arreglo de palabras

# Eliminar stopwords
tokens = []
for token in vector_oracion:
    if token not in stopwords:
        tokens.append(token)


print(tokens)