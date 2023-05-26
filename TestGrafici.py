import matplotlib.pyplot as plt

# Dati per l'asse x (valori di x)
x = [1, 2, 3, 4, 5]

# Dati per l'asse y (valori di y corrispondenti)
y = [2, 4, 6, 8, 10]

# Creazione del grafico a linee
plt.plot(x, y)

# Aggiunta di etichette agli assi
plt.xlabel('X')
plt.ylabel('Y')

# Aggiunta di un titolo al grafico
plt.title('Grafico a Linee')

# Mostra il grafico
plt.savefig('skill_analysis/grafici/grafico.png')
