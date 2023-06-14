from pymongo import MongoClient
import ast

def main():
    
    collection=connection()

    tot = collection.count_documents({})

    doc=dizionarioIdUnici(collection)

    #print(skillNegliAnni(collection))
    #valUnici(collection,tot)
    #addCount100(collection)
    #numCreatorName(collection)
    #argomento(collection)
    #max_addCount(collection,"addCount")
    #print(prime_venti_skill(collection,"addCount"))
    #repetition(collection)
    channelDifferenti(collection,doc)
    #boh(collection,doc)



################MONGODB################
def connection():
    # Connessione a MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['Tesi']
    return db['Tesi']


########################QUERY########################

def dizionarioIdUnici(collection):
    doc={}
    i=0
    #skill con id unico
    pipeline = [{"$group": {"_id": {"id": "$id","trigger":"$triggers", "actions": "$actions","titolo":"$title","creatore":"$creatorName"}, "ripetute": {"$sum": 1}}}]
    result = list(collection.aggregate(pipeline))
    
    for val in result:
        doc[i] = val["_id"]
        i=i+1
    
    return doc

def skillNegliAnni(collection):
    risposta=""
    #date uniche senza ripetizioni
    dateUnici = [
        {"$group": {"_id": "$created", "count": {"$sum": 1}}},
        #{"$group": {"_id": None, "total": {"$sum": 1}}}
    ]
    risultato = list(collection.aggregate(dateUnici))
    anni={"2023":0,"2022":0,"2021":0,"2020":0,"2019":0,"2018":0}
    x=0
    for val in risultato:
        stringa=str(val)
        for chiave, valore in anni.items():
            if str(chiave) in stringa:
                anni[chiave]=anni[chiave]+risultato[x]['count']
        x=x+1

    risposta+=(f'Ci sono sono:')
    for chiave, valore in anni.items():
        risposta+=(f' - {valore} skill nel {chiave}')
    
    return risposta


def valUnici(collection,tot):
    #id unici senza ripetizioni
    idUnici = [
        {"$group": {"_id": "$id", "count": {"$sum": 1}}},
        {"$group": {"_id": None, "total": {"$sum": 1}}}
    ]
    result = list(collection.aggregate(idUnici))

    # Estrai il numero totale di valori unici
    numero_unici = result[0]['total'] if result else 0
    print(f"Il numero di valori unici è: {numero_unici} su {tot} righe")


def addCount100(collection):
    #addCount maggiore di 100
    i=0
    addCount = {'addCount': { "$gt": 100 }}
    ris_addCount = collection.find(addCount)
     # Elaborazione dei risultati
    for result in ris_addCount:
        i=i+1
    print("Ci sono "+ str(i) +" app che sono state aggiunte da più di 100 persone")
    

def numCreatorName(collection):
    #collection
    j=0
    num_cratorName = [{"$group": {"_id": "$creatorName", "conteggio": {"$sum": 1}}}]
    ris_num_creatorName = collection.aggregate(num_cratorName)
    for doc in ris_num_creatorName:
        j=j+1
    print("Ci sono "+ str(j) + " diversi creatorName")


def max_addCount(collection,campo):
    # Esegui la query per trovare il valore massimo
    documento_massimo = collection.find_one({}, sort=[(campo, -1)])
    titolo = documento_massimo["title"]
    # Estrai il valore massimo
    valore_massimo = documento_massimo[campo] if documento_massimo else None
    # Stampa il risultato
    print(f"Il skill {titolo} ha {campo} di: {valore_massimo}")


# suddividiamo le regole per creator, se la regola è ripetutta piu volte
def repetition(collection):

    #skill con id unico
    pipeline = [{"$group": {"_id": {"id": "$id", "creatorName": "$creatorName"}, "ripetute": {"$sum": 1}}}]
    result = list(collection.aggregate(pipeline))

    #stampo skill ripetute più volte
    for doc in result:
        if doc['ripetute'] > 1:
            campo1 = doc['_id']['id']
            campo2 = doc['_id']['creatorName']
            conteggio = doc['ripetute']
            print(f"id: {campo1}, creatorName: {campo2}, ripetute: {conteggio}")


#Da controllare
def prime_venti_skill(collection,campo):
    stringa="le prime 20 skill sono:"

    # Esegui la query per trovare i valori più alti
    #documenti_max = collection.find().sort(campo, -1).limit(20)
    
    pipeline = [
        {"$sort": {campo: -1}},
        {"$limit": 200},
        {"$group": {"_id": {"id": "$id", "creatore": "$creatorName", "titolo":"$title"}, "ripetute": {"$sum": 1}}}
    ]

    results = collection.aggregate(pipeline)
    
    # risultati
    for documento in results:
        stringa+=(f' - {documento["_id"]["titolo"]}')
    return stringa


#WIP
def argomentiPiuRicorrenti(collection):
    #tutte le descrizioni uniche, poi vedo quali sono IoT, quali social, quali business, Twitter, email, insstagram, facebook, note ecc
    #date uniche senza ripetizioni
    #fai un dizionario con vari argomenti, magari quelli dei paper, poi controlli le ripetizioni di quelle parole nelle varie skill

    dizionario={"Instagram":0,
                "Facebook":0,
                "Twitter":0,
                "Google":0,
                "Alexa":0,
                "Calendar":0,
                "Amazon":0,
                "Andorid":0,
                "pics":0,
                "IFTTT":0,
                "Philips":0,
                "Xiaomi":0,
                "Bulb":0,
                "spradsheet":0,
                "Weather":0,
                "iOS":0,
                "location":0,
                "":0,
                "":0,
                "":0}
    
    descUnici = [{"$group": {"_id": "$desc", "count": {"$sum": 1}}}]
    risdesc = list(collection.aggregate(descUnici))
    y=0
    categorie={"Instagram":0,"mail":0,"Iot":0}
    for valore in risdesc:
        
        y=y+1
    return(f'ci sono {y} desc uniche ')


#WIP (stessa regola channel diversi)
# o regole con stesso funzionamento (stesso actionId), però con channel diversi (actionChannelId) (servizi)
#stesso trigger stessi action, il trigger è un evento, definire quanto simili solo action e trigger
# "accendere la luce" ma magari scritti diversamente
#che hanno lo stesso comportamento
#channel diversi sarebbero servizi diversi 
#channel sono i servizi, sia per trigger che per action
#a parità di azione quanti servizi ci sono che fanno cose diverse
#es. xiaomi e philips (sono i channel) quante regole ci sono che accendono le lampadine con trigger e action simile ma channel () diverso
# cluster con tutte regole simili in un unico file 
def channelDifferenti(collection,doc):
    
    #COME CONTO IL NUM DI ACTION? COME PRENDO SOLO I CHANNEL?
    print(doc[0]['actions'])


#WIP (come lo faccio a capire? scrivi per mail per chiarimenti, mi devo basare sulla transitività? come arrivo a un punto A a un punto B attraverso più regole?)
#
# se definisco tante regole, ma definendone di meno potrei avere lo stesso servizio

#se l'action di una regola è simile al trigger di un'altra regola
#
def boh(collection,doc):

    #devo controllare per ogni trigger le varie action, magari farlo per un num limitato
    return
    
    


#query di test
def test(collection,tot):
    #ProPublica quante skill ha fatto
    creatorNmae = {'creatorName': 'ProPublica'}
    ris_creatorName = collection.count_documents(creatorNmae)
    print("il craetor ProPublica ha fatto "+ str(ris_creatorName) +" skill")

    #quanti con creatorUrl?
    creatorUrl = {"creatorUrl": {"$regex": "ifttt", "$options": "i"}}
    ris_creatorUrl = collection.count_documents(creatorUrl)
    print("ci sono "+ str(ris_creatorUrl) +" url di creator su "+ str(tot) +" linee")
    return


# Chiamata alla funzione main nel contesto globale
if __name__ == "__main__":
    main()
