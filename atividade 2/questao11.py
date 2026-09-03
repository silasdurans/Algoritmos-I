nota = int(input("Qual sua nota? "))
frequencia = float(input("Qual sua frequência de 0 a 100? "))/100

aprovado = nota >= 7 and frequencia >= 0.75

print("Você foi aprovado?", aprovado)