import socket
import time


def enviar():  #Cliente
    IP = input('IP: ')
    PORT = int(input('Porta: '))
    PACKAGE = int(input('Tamanho do pacote: ')) #1500, 100 ou 500
    FILE = input('Nome do arquivo: ')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Cria o socket do cliente
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Ajusta o socket para permitir reconexão no mesmo (IP, PORT)
    client_socket.connect((IP, PORT))   #Faz a conexão com o servidor

    f = open(f'./enviado/{FILE}', 'rb')

    package_size = PACKAGE
    package_number = 0
    package = f.read(package_size)

    transmission_start = time.time()
    while package:
        package_number += 1
        print(f'Enviando pacote {package_number}')
        client_socket.send(package)
        package = f.read(package_size)

    transmission_end = time.time()
    transmission_time = transmission_end - transmission_start

    f.close()
    print('\nArquivo enviado com sucesso!')
    print(f'Tamanho do arquivo: {package_number * package_size} Bytes')
    print(f'Número de Pacotes transmitidos: {package_number}')
    print(f'Velocidade de Transmissão: {round((package_number * package_size * 8) / PACKAGE / transmission_time, 2)} kb/s') #Multiplicado por 8 para converter Bytes para Bits

    client_socket.shutdown(socket.SHUT_WR)
    client_socket.close()


def receber(): #Servidor
    IP = input('IP: ')
    PORT = int(input('Porta: '))
    PACKAGE = int(input('Tamanho do pacote: ')) #1500, 100 ou 500
    FILE = input('Nome do arquivo: ')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Cria o socket do servidor
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #Ajusta o socket para permitir reconexão no mesmo (IP, PORT)

    server_socket.bind((IP, PORT))

    f = open(f'./recebido/{FILE}', 'wb')

    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Conexão estabelecida de ({addr})')

        package_size = PACKAGE
        package_number = 0
        package = client_socket.recv(package_size)

        transmission_start = time.time()
        while package:
            package_number += 1
            print(f'Recebendo pacote {package_number}')
            f.write(package)
            package = client_socket.recv(package_size)

        transmission_end = time.time()
        transmission_time = transmission_end - transmission_start

        f.close()
        print('\nArquivo recebido com sucesso!')
        print(f'Tamanho do arquivo: {package_number * package_size} Bytes')
        print(f'Número de Pacotes recebidos: {package_number}')
        print(f'Velocidade de Transmissão: {round((package_number * package_size * 8) / PACKAGE / transmission_time, 2)} kb/s') #Multiplicado por 8 para converter Bytes para Bits

        client_socket.close()
        break
    

def menu():
    print("Escolha uma opção\n")
    print("1 - Enviar arquivo")
    print("2 - Receber arquivo")
    print("3 - Sair da aplicação")



def main():
    while True:
        menu()
        op = int(input())

        if op == 1:
            enviar()
        elif op == 2:
            receber()
        elif op == 3:
            print("Saindo do app. . .")
            return
        
main()
        




    