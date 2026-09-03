# -------------------- Questão 1 --------------------
nome = "Silas Almeida Durans Lima"
curso = "ABI - Área Básica de Ingresso"

print("Olá, meu nome é", nome, "e estou cursando", curso)

# -------------------- Questão 2 --------------------
largura = 4
comprimento = 5
area = largura * comprimento
print(area)

comprimento = 10
area = largura * comprimento
print(area)

# -------------------- Questão 3 --------------------
x = 15
y = 30
aux = x

print(x, y)  # valor original de x e y

x = y
y = aux

print(x, y)  # valor trocado de x e y

# -------------------- Questão 4 --------------------
p1 = "Café"
p2 = "Açucar"

print(p1, p2)  # valor original de p1 e p2

p1, p2 = p2, p1

print(p1, p2)  # valor trocado de p1 e p2

# -------------------- Questão 5 --------------------
num1 = 17
num2 = 4

print("O resultado da divisão real = ", num1 / num2)
print("O resultado da divisão inteira = ", num1 // num2)
print("O resultado do resto da divisão = ", num1 % num2)
print("O resultado de num1 elevado a num2 = ", num1 ** num2)

# -------------------- Questão 6 --------------------
pontos = 100
pontos += 50
pontos -= 20
pontos *= 2
pontos /= 4

print("pontuação final = ", pontos)

# -------------------- Questão 7 --------------------
num_str = "250"
num_str = int(num_str)

num_str += 50

print(num_str)

# -------------------- Questão 8 --------------------
idade = input("Adicione sua idade: ")
idade = int(idade)

print("A idade informada foi:", idade)

# -------------------- Questão 9 --------------------
preco_unidade = float(input("Adicione o preço do produto: "))
quantidade_comprada = int(input("Quantidade comprada: "))

print("Subtotal da compra: R$ ", preco_unidade * quantidade_comprada)

# -------------------- Questão 10 --------------------
ano_nascimento = int(input("Adicione seu ano de nascimento: "))
ano_atual = 2026

idade = ano_atual - ano_nascimento
maior_de_idade = idade >= 18

print(idade)
print(maior_de_idade)

# -------------------- Questão 11 --------------------
nota = int(input("Qual sua nota? "))
frequencia = float(input("Qual sua frequência de 0 a 100? "))

aprovado = nota >= 7 and frequencia >= 75

print("Você foi aprovado?", aprovado)
