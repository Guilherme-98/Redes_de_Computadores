import socket
import time
import math
import os


def enviar():  # Cliente
    IP = input('IP: ')
    PORT = int(input('Porta: '))
    PACKAGE = int(input('Tamanho do pacote: '))  # 1500, 100 ou 500
    FILE = input('Nome do arquivo: ')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Cria o Socket de protocolo UDP

    f = open(f'./enviado/{FILE}', 'rb')

    ADDR = (IP, PORT)
    TRANSMISSION_WINDOW = 4 #Quantidade de pacotes a serem enviados por vez
    HEADER_SIZE = 16
    PAYLOAD_SIZE = PACKAGE - HEADER_SIZE

    f.seek(0, 2)
    FILE_SIZE = f.tell()
    f.seek(0)

    TOTAL_PACKAGES = math.ceil(FILE_SIZE / PAYLOAD_SIZE)

    package_counter = 1

    transmission_start = time.time()

    client_socket.sendto(FILE.encode(), ADDR)  # Envia o nome do arquivo

    # Envia o tamanho do arquivo
    client_socket.sendto(str(FILE_SIZE).encode(), ADDR)

    # Envia o número total de pacotes
    client_socket.sendto(str(TOTAL_PACKAGES).encode(), ADDR)

    while package_counter - 1 < TOTAL_PACKAGES:
        for i in range(TRANSMISSION_WINDOW):
            payload = f.read(PAYLOAD_SIZE)
            # Faz um header com caracteres com o contador de pacotes em hexadecimal
            header = bytes('{:0>16}'.format(format(package_counter, 'X')), 'utf-8')
            package = b''.join([header, payload])

            client_socket.sendto(package, ADDR)
            print(f'Enviando pacote {package_counter}')

            package_counter += 1

        client_socket.recvfrom(PACKAGE)

    client_socket.sendto(b'END!', ADDR)

    f.close()
    client_socket.close()

    transmission_end = time.time()
    transmission_time = transmission_end - transmission_start

    print('\nArquivo enviado com sucesso!')
    print(f'Tamanho do arquivo: {FILE_SIZE / PACKAGE} kB')
    print(f'Número de Pacotes transmitidos: {TOTAL_PACKAGES}')
    print(f'Tamanho dos Pacotes: {PACKAGE}')
    print(f'Tamanho da Janela de Transmissao: {TRANSMISSION_WINDOW}')

    # Multiplicado por 8 para converter Bytes para Bits
    print(f'Velocidade de Transmissão: {round((TOTAL_PACKAGES * PACKAGE * 8) / 1024 / transmission_time, 2)} kb/s')


def receber():  # Servidor
    IP = input('IP: ')
    PORT = int(input('Porta: '))
    PACKAGE = int(input('Tamanho do pacote: '))  # 1500, 100 ou 500
    FILE = input('Nome do arquivo: ')    

    # Cria o socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Ajusta o socket para permitir reconexão no mesmo (IP, PORT)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((IP, PORT))

    
    TRANSMISSION_WINDOW = 4 #Quantidade de pacotes a serem enviados por vez
    HEADER_SIZE = 16
    PAYLOAD_SIZE = PACKAGE - HEADER_SIZE

    transmission_start = time.time()

    data, client_addr = server_socket.recvfrom(PACKAGE)
    FILE = data.decode()

    data, client_addr = server_socket.recvfrom(PACKAGE)
    FILE_SIZE = int(float(data.decode()))

    data, client_addr = server_socket.recvfrom(PACKAGE)
    TOTAL_PACKAGES = int(data.decode())

    package_list = {}

    f = open(f'./recebido/{FILE}', 'wb')

    total_packages_counter = 0
    while True:
        counter = 0

        while counter < TRANSMISSION_WINDOW:
            data, client_addr = server_socket.recvfrom(PACKAGE)
            print(f'Recebendo pacote {total_packages_counter + counter + 1}')

            if '0000000000000000' in str(data)[:16]:
                print('Pacote nulo recebido.')
                break

            index = int(str(data)[2:HEADER_SIZE+2], 16)
            package_list[index] = data[HEADER_SIZE:]

            counter = counter + 1

        if '0000000000000000' in str(data)[:16]:
            print('Pacote nulo recebido.')
            break
        
        window_package_counter = index - TRANSMISSION_WINDOW + 1
        
        while True:
            f.write(package_list[window_package_counter])
            window_package_counter = window_package_counter + 1

            if(window_package_counter == index + 1):
                package_list.clear()
                break
        
        server_socket.sendto(b'RECEIVED!', client_addr)

        total_packages_counter = total_packages_counter + TRANSMISSION_WINDOW
        if total_packages_counter >= TOTAL_PACKAGES:
            break

    f.close()
    server_socket.close()

    transmission_end = time.time()
    transmission_time = transmission_end - transmission_start

    print('\nArquivo recebido com sucesso!')
    print(f'Tamanho do arquivo: {FILE_SIZE / 1024} kB')
    print(f'Número de Pacotes transmitidos: {TOTAL_PACKAGES}')
    print(f'Tamanho dos Pacotes: {PACKAGE}')
    print(f'Tamanho da Janela de Transmissao: {TRANSMISSION_WINDOW}')

    #Multiplicado por 8 para converter Bytes para Bits
    print(f'Velocidade de Transmissão: {round((TOTAL_PACKAGES * PACKAGE * 8) / 1024 / transmission_time, 2)} kb/s') 
            


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
