import pandas as pd
from nltk.corpus import stopwords
from NLP_Utils import TukeyNLP
import numpy as np

# Lectura del archivo y construcción de dataset
with open("Examen/test.txt", "r", encoding="utf-8") as f:
    corpus = f.readlines()
data = []
for line in corpus:
    if ";" in line:
        phrase, feeling = line.strip().split(";")
        data.append({"texto": phrase, "feeling": feeling})
df = pd.DataFrame(data)

# Normalizar los documentos
stopwords_to_add = [
    'just', 'would', 'really', 'like', 'get', 'got', 'going', 'went',
    'make', 'makes', 'made', 'even', 'well', 'lot', 'thing', 'things',
    'something', 'anything', 'everything', 'nothing',
    'one', 'two', 'three', 'four', 'five', 'first', 'second', 'last',
    'said', 'say', 'says', 'don', 'does', 'did', 'doing', 'done',
    'was', 'were', 'been', 'am', 'are', 'is', 'be', 'being',
    'has', 'have', 'had', 'having',
    'could', 'should', 'would', 'may', 'might', 'must',
    'can', 'will', 'shall','intr',
    'some', 'most', 'many', 'few', 'more', 'much', 'less',
    'every', 'each', 'another', 'other', 'others', 'such',
    'also', 'still', 'yet', 'ever', 'never', 'always', 'sometimes',
    'often', 'usually', 'maybe', 'perhaps',
    'please', 'sure', 'really', 'very', 'quite', 'too',
    'around', 'again', 'away', 'back', 'out', 'up', 'down', 'off', 'on', 'in', 'over', 'under', 'through', 'into',
    'there', 'here', 'where', 'when', 'why', 'how',
    'yes', 'no', 'okay', 'ok','im', 'feel', 'feeling', 'ive', 
    'lot', 'thing', 'way', 'place', 'time','dont','bit','teh',
    'something', 'someone', 'anyone', 'everyone', 'nobody'
]
nlp = TukeyNLP(stopwords_extra=stopwords_to_add)
df["tokens"] = df["texto"].apply(nlp.normalizar_documento)

# Filtro por emoción los tokens para así llevar una clasificacion
df_feelings = df.groupby("feeling")["tokens"].apply(lambda x: sum(x, []))
corpus_tokens = df_feelings.tolist()

# Obtengo la matriz de Bag Of Words
vocabulary, bow = nlp.get_bow(corpus_tokens)
bow_df = pd.DataFrame(bow, index=df_feelings.index, columns=vocabulary)

# Obtengo la matriz de TF-IDF
tf_idf_matrix = nlp.tf_idf(corpus_tokens, vocabulary)
tf_idf_df = pd.DataFrame(tf_idf_matrix, index=df_feelings.index, columns=vocabulary)


# Análisis
print("\nANALISIS\n")
# Palabras de mayor peso por emoción según TF-IDF, 
print("\nPALABRAS DE MAYOR PESO POR EMOCIÓN: ")
for feel in tf_idf_df.index:
    row = tf_idf_df.loc[feel]
    heaviest_words = row.sort_values(ascending=False).head(10)
    print(f"\nPalabras con mayor peso de '{feel}':")
    print(heaviest_words.index.tolist())

# Busqueda de palabras compartidas entre emociones
# Por simplicidad solo imprimiré las primeras 10 palabras que se repiten en más de una emoción, pero se puede cambiar el parámetro
shared_tokens = []
for word in bow_df.columns:
    count = (bow_df[word] > 0).sum()
    if count >= 2:
        shared_tokens.append(word)
print("\nPALABRAS QUE SE REPITEN ENTRE EMOCIONES: ")
print(shared_tokens[:10])

# Para ver si hay distintos significados en las palabras
# analizaré si hay diferencias grandes en el TF-IDF entre las emociones,
# ya que esto indicaría diferencias en relevancia de forma general y por ende puede ser de significado.
print("\nPALABRAS CON SIGNIFICADO DIFERENTE ENTRE EMOCIONES:")
important_words = {}
min_tf_idf = 0.01  # Valor para que se tome relevante el tf-idf  
relative_difference = 2    # Deben ser el doble de grandes las maximas tf-idfs para que se consideren
for word in tf_idf_df.columns:
    column = tf_idf_df[word]                
    max_value = column.max()                 
    main_feeling = column.idxmax()          
    if max_value < min_tf_idf:
        continue                            
    other_values = column.drop(main_feeling)  
    average_others = other_values.mean()      
    if average_others != 0 and (max_value / average_others >= relative_difference):
        important_words[word] = main_feeling
for word, feeling in important_words.items():
    print(f"'{word}' destaca en '{feeling}' por tener mucho mas peso de tf-idf a comparacion de las demas")

# Palabras que más salen en todo el corpus
print("\nPALABRAS MÁS REPETIDAS EN TODO EL CORPUS:")
bow_array = np.array(bow)
total_frequencies = bow_array.sum(axis=0) 
top_indices = total_frequencies.argsort()[::-1][:10]  
for idx in top_indices:
    print(f"{vocabulary[idx]}: {total_frequencies[idx]}")

# Longitud promedio de oraciones por clase
df["longitud"] = df["tokens"].apply(len)
print("\nLONGITUD PROMEDIO DE ORACIONES POR EMOCIÓN:")
print(df.groupby("feeling")["longitud"].mean())

# Palabras exclusivas de cada emoción
# Por simplicidad solo imprimiré 10 de cada una, aunque se puede modificar el parámetro
print("\nPALABRAS EXCLUSIVAS POR EMOCIÓN:")
for emotion in bow_df.index:
    exclusivas = []
    for word in bow_df.columns:
        if bow_df.loc[emotion, word] > 0 and (bow_df[word] > 0).sum() == 1:
            exclusivas.append(word)
    print(f"{emotion}: {exclusivas[:10]}")  

'''
7) Conclusiones por emoción:
Anger: Refleja principalmente frustración y hartazgo, las palabras más comunes suelen ir relacionadas con las posibles razones,
las cuales van desde cuestiones de citas, intrapersonales e incluso destaca la mención de JavaScript.

Fear: Esta clase parece enfocarse mucho en el miedo relacionado a las inseguridades propias, mencionando aspectos físicos e incluso
de salud, como el asma.

Joy: Se destaca la alusión a la autorrealización, la tranquilidad y sensaciones positivas o aspectos bien vistos o reconocidos por la
sociedad, que en algunas ocasiones podrían asociarse a cosas como el éxito o la estabilidad.

Love: Palabras principalmente con características positivas en una persona, cosas que normalmente es bueno encontrarlas
en aquellos con quienes se convive, así como cualidades referentes al romanticismo.

Sadness: Se hace referencia principalmente a palabras que reflejan una baja autoestima, muchas relacionadas con
la visión de los demás, como no bienvenido, avergonzado, etc.

Surprise: Las palabras muestran cosas más que nada formas de describir cosas peculiares o extrañas, además
de que destacaron bastante por su idf la palabra curioso y extraño.


8) Finalmente puedo decir que hay mucho vocabulario compartido, sin embargo al aplicar algoritmos que asignan
   pesos como TF-IDF se encuentran de mejor manera aquellas palabras representativas de cada clase y en el top
   de palabras con mayor peso por emoción realmente no pude encontrar repeticiones entre las distintas clases.
   Respecto a emociones que tuvieran palabras con un peso mayor respecto a las demás, destacó surprise que tuvo
   las dos palabras con mayor diferencia de peso dado por TF-IDF, lo que también puede implicar un uso distintivo
   de las mismas al estar referidas en esta emoción.
   En relación a la longitud de las oraciones, el promedio de todas se encuentra entre 6 y 7, lo que indica que
   el texto entre cada emoción es más o menos uniforme.
'''