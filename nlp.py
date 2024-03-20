# Importez les modules requis
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

def enregistrement_nlp(res_speech):
    
    # Initialisation des variables à des valeurs par défaut
    ville = None  
    date = None

    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
    nlp2 = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    
    # Analyser la retranscription vocale avec NLP
    test_nlp = nlp2(res_speech)
    
    # Parcourir les résultats de l'analyse NLP
    for i in test_nlp:
        if i["entity_group"] == 'LOC':
            print(i["word"])
            ville = i["word"]
        elif i["entity_group"] == "DATE":
            print(i["word"])
            date = i["word"]
    
    # Retourner les résultats
    return {"ville": ville, "date": date}


