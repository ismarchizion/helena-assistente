# tools/conhecimento_medico.py

def buscar_informacao_medica(query):
    # Aqui você pode futuramente conectar com bases como UpToDate, APIs médicas, etc.
    base_simulada = {
        "diabetes tipo 1": "É uma doença autoimune onde o pâncreas não produz insulina.",
        "insulina": "Hormônio responsável por controlar a glicose no sangue.",
        "hipoglicemia": "Nível baixo de glicose no sangue, abaixo de 70 mg/dL."
    }

    for termo, resposta in base_simulada.items():
        if termo in query.lower():
            return resposta
    return "Desculpe, não encontrei informações sobre esse termo ainda."
