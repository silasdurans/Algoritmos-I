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