from pymongo import MongoClient
import Levenshtein

class CategoriaAnnue:
    def __init__(self, categoria, anno):
        self.nome = categoria
        self.eta = anno

def main():
    
    collection=connection()

    tot = collection.count_documents({})

    doc=dizionarioIdUnici(collection)

    #print(skillNegliAnni(collection)) #<-controlla
    #valUnici(collection,tot) #<- done
    #addCount100(collection) #<- fai prime 20 skill più scaricate
    #numCreatorName(collection) #<- fai i primi 20 craetor name per numero di skill scaricate
    #max_addCount(collection,"addCount") #<-LA skill più scaricata
    #print(prime_venti_skill(collection,"addCount")) #<- done
    #argomentiPiuRicorrenti(collection,doc) #<- done
    #channelDifferenti(collection,doc) #<- done
    #privacy(doc) #<- done
    #iotapp(doc) #<- done
    #appletAnnue(doc) #<- done


    #repetition(collection)
    #argomento(collection) #<-???
    #boh(collection,doc)



################MONGODB################
def connection():
    # Connessione a MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['Tesi']
    return db['TesiV2']


################################################

#le sole applet ripetute una sola volta
def dizionarioIdUnici(collection):
    doc={}
    i=0
    #skill con id unico
    pipeline = [{"$group": {"_id": {"id": "$id","trigger":"$triggers", "actions": "$actions","titolo":"$title","creatore":"$creatorName","dataCreata":"$created"}, "ripetute": {"$sum": 1}}}]
    result = list(collection.aggregate(pipeline))
    
    for val in result:
        doc[i] = val["_id"]
        i=i+1
        
    return doc

########################QUERY########################

#numero applet create negli anni
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
        risposta+=(f' - {valore} applet nel {chiave}')
    
    return risposta


#applet uniche (come ho fatto per doc, un po' useless)
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


#applet scaricate più di 100volte
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
    print(f"l'applet {titolo} ha {campo} di: {valore_massimo}")


# suddividiamo le regole per creator, se la regola è ripetutta piu volte
def repetition(collection):

    #skill con id unico
    pipeline = [{"$group": {"_id": {"id": "$id", "creatorName": "$creatorName"}, "ripetute": {"$sum": 1}}},{"$sort":{"ripetute":1}}] 
    result = list(collection.aggregate(pipeline))

    #stampo skill ripetute più volte
    with open("outputIdRepetition.txt", "w") as file:
        for doc in result:
            if doc['ripetute'] > 1:
                campo1 = doc['_id']['id']
                campo2 = doc['_id']['creatorName']
                conteggio = doc['ripetute']
                file.write(f"\nid: {campo1}, creatorName: {campo2}, ripetute: {conteggio}")
                #print(f"\nid: {campo1}, creatorName: {campo2}, ripetute: {conteggio}")


#prima 20 skill più scaricate - Da controllare
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
    i=1
    for documento in results:
        stringa+=(f'\n -{i} {documento["_id"]["titolo"]}')
        i=i+1
    return stringa


#divisione applet per categorie
def argomentiPiuRicorrenti(collection,doc):
    #tutte le descrizioni uniche, poi vedo quali sono IoT, quali social, quali business, Twitter, email, insstagram, facebook, note ecc
    #date uniche senza ripetizioni
    #fai un dizionario con vari argomenti, magari quelli dei paper, poi controlli le ripetizioni di quelle parole nelle varie skill

    dizionario={"open":0,
                "close":0,
                "volume down":0,
                "music":0,
                "volume up":0,
                "Google":0,
                "Alexa":0,
                "Calendar":0,
                "Amazon":0,
                "photo":0,
                "IFTTT":0,
                "alarm":0,
                "conditioner":0,
                "Bulb":0,
                "color":0,
                "Weather":0,
                "location":0,
                "tweet":0,
                "post":0,
                "turn on":0,
                "turn off":0}
    i=0
    
    for i in range(len(doc)):
        try:
            stringa = doc[i]['actions']
            dizionarioAppoggio = eval(stringa[1:-1])
            if isinstance(dizionarioAppoggio["actionTitle"],str):
                for chiave in dizionario:
                    if chiave.lower() in dizionarioAppoggio["actionTitle"].lower():
                        dizionario[chiave]+=1
        except Exception as e:
            pass
        
        i+=1   
    
    print(dizionario)


#stessa regola channel diversi
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

    i=0
    simile=0
    ratio=0
    percentuale=0.8

    with open("file.txt", "w") as file:
        file.write(f"range di confronto {len(doc)}*{len(doc)} con percentuale di similarità del {percentuale}%")
        file.write("\n")

        for i in range(len(doc)):
            j=0
            try:

                stringa1 = doc[i]['actions']
                stringaAppoggio1 = eval(stringa1[1:-1])

                if isinstance(stringaAppoggio1["actionTitle"],str): #controllo se stringa valida

                    #mi vado a prendere la seconda stringa
                    for j in range(len(doc)):        
                        if j!=i: #non mi serve confrontare la stringa con se stessa
                        
                            stringa2 = doc[j]['actions']
                            stringaAppoggio2 = eval(stringa2[1:-1])
                            
                            if isinstance(stringaAppoggio2["actionTitle"],str): #controllo se stringa valida
                                    #aumenta solo se c'è l'effettivo confronto fra stringhe
                                    ratio+=1           

                                    #inizio il calcolo della differenza fra le due stringe
                                    distanza = Levenshtein.distance(stringaAppoggio1["actionTitle"], stringaAppoggio2["actionTitle"])
                                    similarita = 1 - (distanza / max(len(stringaAppoggio1["actionTitle"]), len(stringaAppoggio2["actionTitle"])))
                                    
                                    if similarita > percentuale:
                                        file.write(f'{stringaAppoggio1["actionTitle"]} --- simile al {percentuale}% alla stringa --- {stringaAppoggio2["actionTitle"]}')
                                        file.write("\n")
                                        simile+=1
                                    
                        j+=1

            except Exception as e:
                pass
            
            i+=1   
        
        prob=(simile/ratio)*100

        file.write("\n")
        file.write(f'{simile} stringe simili al {percentuale}% su {ratio} confronti per una percentuale di {prob}%')

    print(f'{simile} stringe simili al {percentuale}% su {ratio} confronti per una percentuale di {prob}%')


#controllare la privacy delle skill, quante richiedono accesso a email o postare su twitter che non sono di google (email) o Twitter (post a tweet)
def privacy(doc):
    i=0
    noGoogle = 0
    noTwitter = 0
    noPhoto = 0
    for i in range(len(doc)):
        try:
            stringa1 = doc[i]['actions']
            stringaAppoggio1 = eval(stringa1[1:-1])
            actionTitle=stringaAppoggio1["actionTitle"]

            if isinstance(actionTitle,str): #controllo se stringa valida
                if "Google" not in stringaAppoggio1['actionChannelTitle'] and "email" in actionTitle:
                    noGoogle+=1
                if "Twitter" not in stringaAppoggio1['actionChannelTitle'] and "tweet" in actionTitle:
                    noTwitter+=1
                if "Google" not in stringaAppoggio1['actionChannelTitle'] and "photo" in actionTitle:
                    noPhoto+=1

        except Exception as e:
            pass
        
        i+=1

    print(f'il numero di action che potrebbero violare la privacy in quanto non sono delle seguenti aziende ma compiono azioni quali "mandare mail" / "postare su twitter" / "usare foto" sono:  Google = {noGoogle} --- Twitter = {noTwitter} --- Photo = {noPhoto}')

#tutte le applet prettamente iot
def iotapp(doc):
    iot=0
    keyword = ["turn on","light","turn off","iot"]
    for i in range(len(doc)):
        try:
            stringa1 = doc[i]['actions']
            stringaAppoggio1 = eval(stringa1[1:-1])
            actionDesc=stringaAppoggio1["actionDesc"]
            if isinstance(actionDesc,str): #controllo se stringa valida
                for val in keyword:
                    if val in actionDesc:
                        iot+=1
        except Exception as e:
            pass

        i+=1

    return(print(f'{iot} su {i} applet totali'))


#categorie divise per actiondesc, annue
def appletAnnue(doc):
    risultato=""
    anni=["2023","2022","2021","2020","2019","2018"]
    dizionario={"open":0,
                "close":0,
                "volume down":0,
                "music":0,
                "volume up":0,
                "Google":0,
                "Alexa":0,
                "Calendar":0,
                "Amazon":0,
                "photo":0,
                "IFTTT":0,
                "alarm":0,
                "conditioner":0,
                "Bulb":0,
                "color":0,
                "Weather":0,
                "location":0,
                "tweet":0,
                "post":0,
                "turn on":0,
                "turn off":0}
    #for per ogni anno
    for val in anni:
        for i in range(len(doc)):
            try:
                if val in str(doc[i]['dataCreata']):
                    stringa1 = doc[i]['actions']
                    stringaAppoggio1 = eval(stringa1[1:-1])
                    actionDesc=stringaAppoggio1["actionDesc"]
                    if isinstance(actionDesc,str): #controllo se stringa valida
                            for chiave in dizionario:
                                if chiave.lower() in actionDesc.lower():
                                    dizionario[chiave]+=1
            
            except Exception as e:
                pass

            i+=1
        risultato+=f"per annno {val} i valori delle varie categorie sono {dizionario}"
        risultato+="\n\n"

        for chiave in dizionario:
            dizionario[chiave] = 0

    return (print(risultato))


#TODO
def categoriePercentuali(doc):
    keyword=["light"]
    dizionarioCat={"trigger":0,"voice":0,"button":0,"time":0,"weather":0,"other":0}


        #COME CONTO IL NUM DI ACTION? COME PRENDO SOLO I CHANNEL?
    #stringa = doc[0]['actions']
    #dizionario = eval(stringa[1:-1])
    #print(dizionario["actionChannelTitle"])

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
