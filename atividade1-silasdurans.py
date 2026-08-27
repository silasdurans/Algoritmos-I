# Algoritmo: Fazendo um misto
#PseudoCódigo

# se pao igual a sim
#   voce tem o pao
#   se faca igual a sim
#       voce tem a faca
#       se queijo e presunto igual a sim
#           voce tem um misto
#       senao se queijo for sim e presunto nao
#           voce tem um misto so de queijo
#       senao se queijo nao e presunto sim
#           voce tem um misto so de presunto
#       senao
#           voce tem um misto so de presunto
#   senao
#       voce nao tem a faca
#senao
#   voce nao pode fazer um misto sem pao

pao = input("Você tem pão? S/N: ").upper()
queijo = input("Você tem queijo? S/N: ").upper()
presunto = input("Você tem presunto? S/N: ").upper()
faca = input("Você tem faca? S/N: ").upper()

if pao == 'S':
    print('Você tem o pão')
    if faca == 'S':
        print('Você tem a faca')
        if queijo == 'S' and presunto == 'S':
            print('Você tem um misto de queijo e presunto')
        elif queijo == 'S' and presunto == 'N':
            print('Você tem um misto só de queijo')
        elif queijo == 'N' and presunto == 'S':
            print('Você tem um misto só de presunto')
        else:
            print('Você não tem queijo nem presunto, não dá pra fazer o misto')
    else:
        print('Você não tem a faca, não da para cortar o pão')
else:
    print('Você não pode fazer um misto sem pão')