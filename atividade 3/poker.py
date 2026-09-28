valor_car1 = int(input("digite o valor da carta 1: "))
valor_car2 = int(input("digite o valor da carta 2: "))
valor_car3 = int(input("digite o valor da carta 3: "))

naipe_car1 = input("naipe da carta? C,O,P,E: ").upper()
naipe_car2 = input("naipe da carta? C,O,P,E: ").upper()
naipe_car3 = input("naipe da carta? C,O,P,E: ").upper()

#verificar valores validos > 1 e < 13
if ((valor_car1 >= 1 and valor_car2 >= 1 and valor_car3 >= 1) and (valor_car1 <= 13 and valor_car2 <= 13 and valor_car3 <= 13)):

    #verificar naipe Copas, Ouros, Paus, Espadas
    if (naipe_car1 == "C" or naipe_car1 == "O" or naipe_car1 == "P" or naipe_car1 == "E") and (naipe_car2 == "C" or naipe_car2 == "O" or naipe_car2 == "P" or naipe_car2 == "E") and (naipe_car3 == "C" or naipe_car3 == "O" or naipe_car3 == "P" or naipe_car3 == "E") :

        #checar maior, menor, meio
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

        #checar mãos
        if menor+1 == meio and meio+1 == maior and naipe_car1 == naipe_car2 == naipe_car3:
            print('STRAIGHT FLUSH')
        elif valor_car1 == valor_car2 == valor_car3:
            print('TRINCA')
        elif menor+1 == meio and meio+1 == maior:
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
