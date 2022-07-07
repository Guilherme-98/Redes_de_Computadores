import socket
import datetime

def enviar():
    
    IP = input('IP: ')
    PORT = int(input('Porta: '))
    PACKAGE_SIZE = 500
    
    package = b'teste de rede *2022*' * 25

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP,PORT))
    sock.listen(0)
    print(f'\nEscutando em: {IP}  Porta:{PORT}\n')

    client_sock, client_addr = sock.accept()
    starttime = datetime.datetime.now()
    package_count = 0
    print_count = 1

    print("###        UPLOAD      ###")
    print("###  Enviando pacotes  ###\n")

    while True:
        client_sock.send(package)
        package_count = package_count + 1
        endtime = datetime.datetime.now()
        delta = endtime - starttime

        if(delta.seconds >= print_count):
            print_count = print_count + 1
            print('.', end='', flush=True)

        if(delta.seconds >= 20):
            client_sock.close()
            break       
    
    print('\n')
    client_sock.close()
    endtime = datetime.datetime.now()
    bytes_transferred = round(package_count * PACKAGE_SIZE / 1024 / 1024, 2)
    speed = round(bytes_transferred * 8 / delta.seconds, 2) 
    velocidade_pacote = round(package_count/delta.seconds, 2) 

    print('## RESULTADOS ##')
    print(f'Pacotes Enviados: {package_count}')   
    print(f'Pacotes por segundo enviados : {round(velocidade_pacote, None)}')  
    print(f'Bytes Transferidos: {bytes_transferred} MB')
    print(f'Velocidade de UPLOAD em Kbps: {speed * 1000} Kbps')
    print(f'Velocidade de UPLOAD em Mbps: {speed} Mbps')
    print(f'Velocidade de UPLOAD em Gbps: {speed  / 1000} Gbps')
    print(f'Tempo: {delta.seconds} segundos\n')  

def receber():
    PACKAGE_SIZE = 500
    IP = input('IP: ')
    PORT = int(input('Porta: '))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o socket 
    sock.connect((IP ,PORT)) # Realiza a conexão com o host

    starttime = datetime.datetime.now() # Inicia o tempo de contagem da transmissão
    package_count = 0
    package_total = 0
    print_count = 1
    
    print("\n###        DOWNLOAD     ###")
    print('###  Recebendo pacotes  ###\n')

    packageAux = b'teste de rede *2022*' * 25

    while True:
        data = sock.recv(PACKAGE_SIZE)
        package_total = package_total + 1

        if(data == packageAux):
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
        bytes_transferred_total = round(package_total * PACKAGE_SIZE / 1024 / 1024, 2)
        speed_total = round(bytes_transferred_total * 8 / delta.seconds, 2)
        velocidade_pacote = round(package_count / delta.seconds, 2)                                                                                                                                                                                                                                    

        print('## RESULTADOS ##')
        print(f'Pacotes Recebidos: {package_count}')
        print(f'Pacotes por segundo recebidos: {round(velocidade_pacote, None)}')
        print(f'Bytes Transferidos: {bytes_transferred_total} MB')
        print(f'Velocidade de DOWNLOAD em Kbps: {speed_total * 1000} Kbps')
        print(f'Velocidade de DOWNLOAD em Mbps: {speed_total} Mbps')
        print(f'Velocidade de DOWNLOAD em Gbps: {speed_total / 1000} Gbps')
        print(f'Tempo: {delta.seconds} segundos\n')
        break

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