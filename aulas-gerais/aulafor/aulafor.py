cont = 0
while cont < 10:
    print(cont+1)
    cont+=1
print("Loop has ended")

#loop for
x=[1,2,3,4,5,6,7,8,9,10]
for cont in x:
    print(cont)
print("Loop has ended")



def imprimirimapres():
    soma = 0
    for i in range (1,51):
        if i%2!=0:
            soma+=i
    return print(soma)

imprimirimapres()