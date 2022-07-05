import socket
import datetime

def enviar(): 
    HOST = input('IP: ')
    PORT = int(input('PORTA: '))

    PACKAGE_SIZE = 500
    HEADER_SIZE = 20
    PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST,PORT))

    print(f'\nEscutando em: {HOST}  Porta:{PORT}\n')

    data, client_addr = sock.recvfrom(PACKAGE_SIZE)

    if data == b'CONNECT!':
        sock.sendto(b'CONNECTED!', client_addr)
    else:
        print('A conexão com os hosts não pôde ser feita!')
        exit(1)

    print("###      UPLOAD      ###")
    print("### Enviando pacotes ###\n")

    sock.settimeout(3)
    starttime = datetime.datetime.now()
    package_id = 1
    package_counter = 0
    count_timeout = 0
    print_count = 1
    payload = b'teste de rede *2022*' * 24

    while True:
        header = bytes('{:0>20}'.format(format(package_id, 'X')), 'utf-8') #Faz um header com caracteres com um identificador único para cada pacote, em hexadecimal
        package_id += 1
        package = b''.join([header, payload])

        sock.sendto(package, client_addr)
        package_counter += 1
        endtime = datetime.datetime.now()
        delta = endtime - starttime

        if(delta.seconds >= print_count):
                print_count = print_count + 1
                print('.', end='', flush=True)

        if(delta.seconds >= 20):
            header = bytes('{:0>20}'.format(0), 'utf-8')     #Faz um header com HEADER_SIZE 0's, em hexadecimal
            package = b''.join([header, b'END!'])

            while True: #Caso o não receba a confirmação em um determinado tempo, envia o pacote de novo, até um máximo de 5 vezes
                try:
                    sock.sendto(package, client_addr)
                    package_counter += 1
                    data, client_addr = sock.recvfrom(PACKAGE_SIZE)

                    if data == b'OK!':
                        break
                except socket.timeout:
                    if count_timeout == 5:
                        break
                    else:
                        count_timeout = count_timeout + 1
                        continue
            break
    count_timeout = 0
    while True: #Caso o não receba a confirmação em um determinado tempo, envia o pacote de novo, até um máximo de 5 vezes
        try:
            sock.sendto(str(package_id).encode(), client_addr)
            package_counter += 1
            data, client_addr = sock.recvfrom(PACKAGE_SIZE)

            if data == b'OK!':
                package_counter += 1
                break
        except socket.timeout:
            if count_timeout == 5:
                break
            else:
                count_timeout = count_timeout + 1
                continue

    sock.close()
    bytes_transferred = round(package_counter * PACKAGE_SIZE / 1024 / 1024, 2)
    speed = round(bytes_transferred * 8 / delta.seconds, 2) 
    velocidade_pacote = round(package_counter/delta.seconds, 2)

    print('\n\n## RESULTADO ##')
    print(f'Pacotes Enviados: {package_counter}')
    print(f'Pacotes por segundo enviados: {round(velocidade_pacote, None)}')
    print(f'Bytes Transferidos: {round(bytes_transferred, 2)} MB')
    print(f'Velocidade de UPLOAD em Kbps: {speed * 1000} Kbps')
    print(f'Velocidade de UPLOAD em Mbps: {speed} Mbps')
    print(f'Velocidade de UPLOAD em Gbps: {speed / 1000} Gbps')
    print(f'Tempo: {delta.seconds} segundos\n')

def receber(): 
    HOST = input('Digite o IP que deseja conectar: ')
    PORT = int(input('PORTA: '))
    PACKAGE_SIZE = 500
    ADDR = (HOST, PORT)
    HEADER_SIZE = 20
    PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

    print(f'\nTamanho do HEADER: {HEADER_SIZE}')
    print(f'Tamanho do PAYLOAD: {PAYLOAD_SIZE}\n')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)

    while True: #Caso o não receba a confirmação em um determinado tempo, envia o pacote de novo
        try:
            sock.sendto(b'CONNECT!', ADDR)
            data, server_addr = sock.recvfrom(PACKAGE_SIZE)

            if data:
                break
        except socket.timeout:
            continue
    
    sock.settimeout(None)

    starttime = datetime.datetime.now()
    package_counter = 0
    print_count = 1

    print('###      DOWNLOAD     ###')
    print('### Recebendo pacotes ###\n')

    while True:
        endtime = datetime.datetime.now()
        delta = endtime - starttime
        package, server_socket = sock.recvfrom(PACKAGE_SIZE)
        package_counter = package_counter + 1
        package_id = int(str(package)[2:HEADER_SIZE+2], 16)

        if package_id !=0: 
            if(delta.seconds >= print_count):
                print_count = print_count + 1
                print('.', end='', flush=True)

            continue

        sock.sendto(b'OK!', ADDR)
        data, server_addr = sock.recvfrom(PACKAGE_SIZE)
        sock.sendto(b'OK!', ADDR)
        packages_sended = int(data.decode())

        sock.close()
        packages_lost = packages_sended - package_counter
        bytes_transferred = round(package_counter * PACKAGE_SIZE / 1024 / 1024, 2)
        delta = endtime - starttime
        speed = round(bytes_transferred * 8 / delta.seconds, 2) 
        velocidade_pacote = round(package_counter/delta.seconds, 2)

        print('\n\n## RESULTADO ##')
        print(f'Pacotes Recebidos: {package_counter}')
        print(f'Pacotes por segundo recebidos: {round(velocidade_pacote, None)}')
        print(f'Pacotes Perdidos: {packages_lost}')
        print(f'Bytes Transferidos: {round(bytes_transferred, 2)} MB')
        print(f'Velocidade de DOWNLOAD em Kbps: {speed * 1000} Kbps') #Megabits por segundo
        print(f'Velocidade de DOWNLOAD em Mbps: {speed} Mbps')
        print(f'Velocidade de DOWNLOAD em Gbps: {speed / 1000} Gbps')
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