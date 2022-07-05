import socket
import datetime



def receber():
    ## DOWNLOAD

    PACKAGE_SIZE = 4096
    IP = input('IP: ')
    PORT = int(input('Porta: '))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o socket 
    sock.connect((IP ,PORT)) # Realiza a conexão com o host

    starttime = datetime.datetime.now() # Inicia o tempo de contagem da transmissão
    package_count = 0
    print_count = 1
    
    print('\n### Testando Download ###')
    while True:
        data = sock.recv(PACKAGE_SIZE)
        package_count = package_count + 1

        endtime = datetime.datetime.now()
        delta = endtime - starttime

        if data:
            del data

            if(delta.seconds >= print_count):
                print_count = print_count + 1
                print('.', end='', flush=True)

            continue

        print('\n')
        sock.close()

        endtime = datetime.datetime.now()
        delta = endtime - starttime
        bytes_transferred = round(package_count * PACKAGE_SIZE / 1024 / 1024, 2)
        speed = round(bytes_transferred * 8 / delta.seconds, 2)

        print('## RESULTADO ##')
        print(f'Pacotes Recebidos: {package_count}')
        print(f'Bytes Transferidos: {bytes_transferred} MB')
        print(f'Velocidade Média: {speed} Mbps')
        print(f'Tempo: {delta.seconds} segundos\n')
        break

    ## UPLOAD

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o socket 
    sock.connect((IP ,PORT)) # Realiza a conexão com o host

    starttime = datetime.datetime.now() # Inicia o tempo de contagem da transmissão

    package_count = 0
    print_count = 1
    package = b'x' * PACKAGE_SIZE * 4

    print('### Testando Upload ###')
    while True:
        sock.send(package)
        package_count = package_count + 1

        endtime = datetime.datetime.now()
        delta = endtime - starttime

        if(delta.seconds >= print_count):
            print_count = print_count + 1
            print('.', end='', flush=True)

        if(delta.seconds >= 20):
            break

    print('\n')
    sock.close()

    endtime = datetime.datetime.now()
    delta = endtime - starttime
    bytes_transferred = round(package_count * PACKAGE_SIZE / 1024 / 1024, 2)
    speed = round(bytes_transferred * 8 / delta.seconds, 2)

    print('## RESULTADO ##')
    print(f'Pacotes Enviados: {package_count}')
    print(f'Bytes Transferidos: {bytes_transferred} MB')
    print(f'Velocidade Média: {speed} Mbps')
    print(f'Tempo: {delta.seconds} segundos\n')


def enviar():
    
    IP = input('IP: ')
    PORT = int(input('Porta: '))
    PACKAGE_SIZE = 4096

    package = b'x' * PACKAGE_SIZE * 4

    print("\n### Testando Download ###\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP,PORT))
    sock.listen(0)
    print(f'Escutando em {IP}:{PORT}')

    client_sock, client_addr = sock.accept()

    starttime = datetime.datetime.now()
    print(starttime, end=' ')
    print(f'{client_addr[0]}:{client_addr[1]} conectado')

    while True:
        client_sock.send(package)

        endtime = datetime.datetime.now()
        delta = endtime - starttime

        if(delta.seconds >= 20):
            client_sock.close()
            break

    endtime = datetime.datetime.now()
    print(endtime, end=' ')
    print(f'{client_addr[0]}:{client_addr[1]} desconectado\n')

    ## UPLOAD DO CLIENTE
    print("### Testando Upload ###\n")

    sock.listen(0)
    print(f'Escutando em {IP}:{PORT}')

    client_sock, client_addr = sock.accept()

    starttime = datetime.datetime.now()
    print(starttime, end=' ')
    print(f'{client_addr[0]}:{client_addr[1]} conectado')

    while True:
        data = client_sock.recv(PACKAGE_SIZE)
        if data:
            del data
            continue

        client_sock.close()

        endtime = datetime.datetime.now()
        print(endtime, end=' ')
        print(f'{client_addr[0]}:{client_addr[1]} desconectado\n')
        break

    sock.close()

def menu():
    print("Escolha uma opção\n")
    print("1 - Receber dados de transmissão")
    print("2 - Enviar dados de transmissão")
    print("3 - Sair da aplicação")


def main():
    while True:
        menu()
        op = int(input())

        if op == 1:
            receber()
        elif op == 2:
            enviar()
        elif op == 3:
            print("Saindo do app. . .")
            return


main()
