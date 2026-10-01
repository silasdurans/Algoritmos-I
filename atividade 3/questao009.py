# Pedir o dia, mês e ano ao utilizador
dia = int(input("Informe o dia: "))
mes = int(input("Informe o mês: "))
ano = int(input("Informe o ano: "))

e_bissexto = (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)

if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
    max_dias = 31
elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
    max_dias = 30
elif mes == 2:
    if e_bissexto:
        max_dias = 29
    else:
        max_dias = 28
else:
    max_dias = 0 

valida = (ano > 0) and (mes >= 1 and mes <= 12) and (dia >= 1 and dia <= max_dias)

if valida:
    print("A data válida")
else:
    print("A data invalida.")