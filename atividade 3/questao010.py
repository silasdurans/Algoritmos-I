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