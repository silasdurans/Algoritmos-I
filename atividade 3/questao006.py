a = int(input("Lado A do triangulo: "))
b = int(input("Lado B do traingulo: "))
c = int(input("Lado C do traingulo: "))

#checar validade
if a + b > c and a + c > b and b + c > a:
    if a == b == c:
        print("equilatero")
    elif a == b or a == c or b == c:
        print("isoceles")
    else:
        print("escaleno")
else:
    print('triangulo invalido')

