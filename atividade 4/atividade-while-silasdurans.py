n = int(input("Digite um numero inteiro positivo N: "))

for i in range(1, n + 1):
    print(i)

#----------------------------------------------------------------#

soma = 0

while True:
    numero = int(input("Digite um numero inteiro (0 para sair): "))
    if numero == 0:
        break
    soma += numero

print(f"Soma total: {soma}")

#----------------------------------------------------------------#

senha = input("Digite a senha: ")

while senha != "CP2026-2-2":
    print("Senha incorreta, tente novamente")
    senha = input("Digite a senha: ")

print("Acesso liberado")

#----------------------------------------------------------------#

numero = int(input("Digite um numero entre 1 e 10: "))

while numero < 1 or numero > 10:
    print("Valor invalido")
    numero = int(input("Digite um numero entre 1 e 10: "))

for i in range(1, 101):
    print(f"{numero} x {i} = {numero * i}")

#----------------------------------------------------------------#

secreto = int(input("Usuario 1, digite o numero secreto (1 a 100): "))

tentativas = 0
palpite = 0

while palpite != secreto:
    palpite = int(input("Usuario 2, digite o seu palpite: "))
    tentativas += 1
    
    if palpite < secreto:
        print("O numero secreto e maior")
    elif palpite > secreto:
        print("O numero secreto e menor")

print(f"Parabens! Voce acertou em {tentativas} tentativa(s).")

#----------------------------------------------------------------#

numero = int(input("Digite um numero inteiro positivo maior que 1: "))

primeiro_divisor = None

for i in range(2, numero):
    if numero % i == 0:
        primeiro_divisor = i
        break

if numero <= 1:
    print("O numero deve ser maior que 1.")
elif primeiro_divisor is None:
    print(f"O numero {numero} e primo.")
else:
    print(f"O numero {numero} nao e primo. Primeiro divisor encontrado: {primeiro_divisor}")

#----------------------------------------------------------------#

n = int(input("Digite um inteiro positivo: "))

passos = 0
print(n, end="")

while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    print(f", {n}", end="")
    passos += 1

print()
print(f"{passos} passos")

#----------------------------------------------------------------#

n = int(input("Digite um numero inteiro N (de 1 a 20): "))

while n < 1 or n > 20:
    n = int(input("Valor invalido. Digite um numero de 1 a 20: "))

for i in range(n, 0, -1):
    print("*" * i)