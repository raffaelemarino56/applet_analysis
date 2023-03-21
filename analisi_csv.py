import pandas as pd
import plotly.express as px

#https://plotly.com/python/plotly-express/#gallery

with open('./dati.csv') as csv_file:

    df=pd.read_csv(csv_file)

   

    #num azioni create durante gli anni
    df["created"] = pd.to_datetime(df["created"])
    aggiunte_per_giorno = df.groupby("created")["addCount"].sum().reset_index()
    aggiunte_per_giorno = aggiunte_per_giorno.sort_values("created", ascending=True)
    fig1 = px.line(aggiunte_per_giorno, x="created", y=["addCount"], title="Andamento aggiunte al giorno")
    fig1.show()
    """
    #grafico a barre per creatorName
    aggiunte_da_craetore = df.groupby("creatorName")["addCount"].sum().reset_index()
    aggiunte_da_craetore = aggiunte_da_craetore.sort_values("creatorName", ascending=False)
    fig2 = px.bar(aggiunte_da_craetore, x="creatorName", y=["addCount"], title="Num di azioni create per creatore")
    fig2.show()
    """
    
    #grafico a torta che raggruppa per creatorName
    preferenze_per_creatore = df.groupby("creatorName").sum().reset_index()
    preferenze_per_creatore = preferenze_per_creatore.sort_values("creatorName", ascending=False)
    fig3 = px.pie(preferenze_per_creatore, values="creatorName", names="creatorName", title="Distribuzione per creatore")
    #fig3.show()
    fig3.write_image("./fig3.jpeg")

    
    
  