from pymongo import MongoClient
from flask import Flask, render_template

app = Flask(__name__)

# Definisci la route per la visualizzazione dei risultati
@app.route('/risultati')
def main():
    # Connessione a MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['Tesi']
    collection = db['Tesi']

    #query
    addCount = {'addCount': { "$gt": 100 }}
    creatorNmae = {'creatorName': 'ProPublica'}
    num_cratorName = [{"$group": {"_id": "$creatorName", "conteggio": {"$sum": 1}}}]

    #sono tutti ifttt?
    query = {"cratorUrl": {"$regex": "zapier", "$options": "i"}}
    count = collection.count_documents(query)
    risultati.append(count)

    #collection
    ris_num_creatorName = collection.aggregate(num_cratorName)
    ris_addCount = collection.find(addCount)
    ris_creatorName = collection.count_documents(creatorNmae)

    risultati=[]

    i=0
    j=0

    # Elaborazione dei risultati
    for result in ris_addCount:
        i=i+1
    
    for doc in ris_num_creatorName:
        j=j+1

    risultati.append(i)
    risultati.append(ris_creatorName)
    risultati.append(j)
    
    #risultati.append("ci sono "+i+" app che sono state aggiunte da più di 100 persone")
    #risultati.append("il craetor ProPublica ha fatto "+ count+" skill")
    #risultati.append("ci sono "+ j+ " diversi creatorName")
    

    client.close()

    return render_template('risultati.html', risultati=risultati)

if __name__ == '__main__':app.run(port=8080)

