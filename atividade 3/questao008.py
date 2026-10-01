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