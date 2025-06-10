import pandas as pd

class Bayes:
    def naive_bayes(self, event: pd.Series, conditions: pd.DataFrame, conditions_specified: list):
        total = len(event)
        unique_events = event.unique()
        result = []

        for evt in unique_events:
            # Probabilidad P(Evento)
            p_evt = (event == evt).sum() / total

            # Subconjunto donde se cumple el evento 
            condition_subset = conditions[event == evt]
            p_conditions_given_evt = 1

            for i, val in enumerate(conditions_specified):
                columna = conditions.columns[i]
                matching = (condition_subset[columna] == val).sum()
                total_matching = len(condition_subset)

                if total_matching > 0:
                    p = matching / total_matching
                else:
                    p = 0  # Evita división entre 0
                p_conditions_given_evt *= p

            # Probabilidad total usando regla de Naive Bayes
            posterior = p_evt * p_conditions_given_evt
            result.append({
                "Evento": evt,
                "Probabilidad": posterior
            })

        # Normalizar las probabilidades (para que sumen 1)
        total_prob = sum([r["Probabilidad"] for r in result])
        for r in result:
            r["Probabilidad"] = r["Probabilidad"] / total_prob if total_prob > 0 else 0

        resultDF = pd.DataFrame(result).sort_values('Probabilidad', ascending=False)
        return resultDF.iloc[0,0], resultDF

df = pd.DataFrame({
    'Clase': ['Sol', 'Lluvia', 'Sol', 'Nieve', 'Sol', 'Lluvia'],
    'Cielo': ['Despejado', 'Nublado', 'Nublado', 'Nublado', 'Despejado', 'Nublado'],
    'Viento': ['Sí', 'Sí', 'No', 'No', 'No', 'Sí']
})

bayes = Bayes()
maximo, res = bayes.naive_bayes(df['Clase'], df[['Cielo', 'Viento']], ['Nublado', 'Sí'])
print(f'\nDataFrame de resultado de probabilidades:\n {res}')
print(f'\nClima más probable: {maximo}\n')
