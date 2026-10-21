# -------------------- Questão 1 --------------------
idade = int(input("Digite sua idade: "))

if idade < 18:
    print("menor de idade")
elif idade >= 18:
    print("maior de idade")

# -------------------- Questão 2 --------------------
num_int = int(input("Digite em numero inteiro: "))

if num_int % 2 == 0:
    print("par")
else:
    print("impar")

# -------------------- Questão 3 --------------------
nota = int(input("Nota aluno: "))

if nota >= 7:
    print('aprovado')
elif nota >= 5:
    print('recuperação')
else:
    print("reprovado")

# -------------------- Questão 4 --------------------
temp = int(input("Digite a temperatura: "))

if temp > 35:
    print("muito quente")

if temp >= 26 and temp <= 35:
    print("quente")

if temp < 15:
    print("frio")

if temp >= 15 and temp <= 25:
    print("agradavel")

# -------------------- Questão 5 --------------------
ano = int(input("Digite o ano: "))

if ano % 4 == 0:
    if ano % 100 != 0 or ano % 400 == 0:
        print("é bissexto")
else:
    print('não é bissexto')

# -------------------- Questão 6 --------------------
a = int(input("Lado A do triangulo: "))
b = int(input("Lado B do traingulo: "))
c = int(input("Lado C do traingulo: "))

# checar validade
if a + b > c and a + c > b and b + c > a:
    if a == b == c:
        print("equilatero")
    elif a == b or a == c or b == c:
        print("isoceles")
    else:
        print("escaleno")
else:
    print('triangulo invalido')

# -------------------- Questão 7 --------------------
usuario = "admin"
senha = "1234"

user = str(input("Digite o usuario: "))

if user != usuario:
    print('Usuario não encontrado')
else:
    passwd = str(input("Digite a senha: "))
    if senha == passwd:
        print("Acesso concedido")
    else:
        print("Senha incorreta")

# -------------------- Questão 8 --------------------
salario_bruto = float(input("Informe o salário bruto: R$ "))

if salario_bruto <= 2000.00:
    imposto = 0.0
elif salario_bruto <= 3500.00:
    imposto = (salario_bruto - 2000.00) * 0.075
elif salario_bruto <= 5000.00:
    imposto = 112.50 + (salario_bruto - 3500.00) * 0.15
else:
    imposto = 337.50 + (salario_bruto - 5000.00) * 0.225

salario_liquido = salario_bruto - imposto

print(f"Imposto total a pagar: R$ {imposto:.2f}")
print(f"Salário líquido: R$ {salario_liquido:.2f}")

# -------------------- Questão 9 --------------------
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

# -------------------- Questão 10 --------------------
idade = int(input("Informe a idade do cliente: "))
renda = float(input("Informe a renda mensal: R$ "))
valor_emprestimo = float(input("Informe o valor total do empréstimo: R$ "))
parcelas = int(input("Informe a quantidade de parcelas: "))

valor_parcela = valor_emprestimo / parcelas

if renda > 10000.00:
    margem_maxima = 0.40
else:
    margem_maxima = 0.30

idade_valida = (idade >= 18) and (idade <= 70)
renda_valida = renda >= 2000.00
parcela_valida = valor_parcela <= (renda * margem_maxima)

if idade_valida and renda_valida and parcela_valida:
    print("Empréstimo APROVADO!")
else:
    print("Empréstimo NEGADO.")

# -------------------- Poker --------------------
valor_car1 = int(input("digite o valor da carta 1: "))
valor_car2 = int(input("digite o valor da carta 2: "))
valor_car3 = int(input("digite o valor da carta 3: "))

naipe_car1 = input("naipe da carta? C,O,P,E: ").upper()
naipe_car2 = input("naipe da carta? C,O,P,E: ").upper()
naipe_car3 = input("naipe da carta? C,O,P,E: ").upper()

# verificar valores validos > 1 e < 13
if ((valor_car1 >= 1 and valor_car2 >= 1 and valor_car3 >= 1)
        and (valor_car1 <= 13 and valor_car2 <= 13 and valor_car3 <= 13)):

    # verificar naipe Copas, Ouros, Paus, Espadas
    if (naipe_car1 in ("C", "O", "P", "E")
            and naipe_car2 in ("C", "O", "P", "E")
            and naipe_car3 in ("C", "O", "P", "E")):

        # checar maior, menor, meio
        if valor_car1 <= valor_car2 and valor_car2 <= valor_car3:
            menor, meio, maior = valor_car1, valor_car2, valor_car3
        elif valor_car1 <= valor_car3 and valor_car3 <= valor_car2:
            menor, meio, maior = valor_car1, valor_car3, valor_car2
        elif valor_car2 <= valor_car1 and valor_car1 <= valor_car3:
            menor, meio, maior = valor_car2, valor_car1, valor_car3
        elif valor_car2 <= valor_car3 and valor_car3 <= valor_car1:
            menor, meio, maior = valor_car2, valor_car3, valor_car1
        elif valor_car3 <= valor_car1 and valor_car1 <= valor_car2:
            menor, meio, maior = valor_car3, valor_car1, valor_car2
        else:
            menor, meio, maior = valor_car3, valor_car2, valor_car1

        # checar mãos
        if menor + 1 == meio and meio + 1 == maior and naipe_car1 == naipe_car2 == naipe_car3:
            print('STRAIGHT FLUSH')
        elif valor_car1 == valor_car2 == valor_car3:
            print('TRINCA')
        elif menor + 1 == meio and meio + 1 == maior:
            print('SEQUÊNCIA')
        elif naipe_car1 == naipe_car2 == naipe_car3:
            print('FLUSH')
        elif valor_car1 == valor_car2 or valor_car2 == valor_car3 or valor_car3 == valor_car1:
            print("PAR")
        else:
            print("CARTA ALTA")
    else:
        print("Entrada inválida")
else:
    print("Entrada inválida")