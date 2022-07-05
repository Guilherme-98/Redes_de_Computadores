import socket
import select   #Ajuda com I/O de dados
from threading import Thread

def fecharServidor():
    fechar = input('Pressione s para fechar o servidor.\n')
    while(fechar != 's'):
        fechar = input()


#IP = '192.168.0.10'
#PORT = 8888

IP = input("IP: ")
PORT = int(input("Porta: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Cria o socket do servidor
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #Ajusta o socket para permitir reconexão no mesmo (IP, PORT)

server_socket.bind((IP, PORT))
server_socket.listen()

clients_list = {}
inputs_list = [server_socket]

encerrar = Thread(target = fecharServidor)
encerrar.start()

while True:
    #Gerencia a entrada de dados, esperando o canal de entrada notificar que está pronto
    read_sockets, _, exception_sockets = select.select(inputs_list, [], inputs_list)

    if(not encerrar.is_alive()):
        for notified_socket in read_sockets:
            notified_socket.close()
        for notified_socket in exception_sockets:
            notified_socket.close()
        break

    for notified_socket in read_sockets:
        if notified_socket == server_socket:    #Conecta com o cliente e recebe seus dados (usuário e socket)
            client_socket, client_adress = server_socket.accept()

            try:
                user = client_socket.recv(2048)
            except:
                user = False
                
            if user is False:
                continue
            
            inputs_list.append(client_socket)
            clients_list[client_socket] = user

            print(f'Nova conexao aceita de {user.decode("utf-8")} ({client_adress[0]}:{client_adress[1]}).')

        else:   #Recebe a mensagem do cliente
            user = clients_list[notified_socket]
            addr = notified_socket.getpeername()
            addr = f'{addr[0]}:{addr[1]}'
            try:
                message = notified_socket.recv(2048)
            except:
                message = False

            if message is False:
                print(f'Conexao encerrada de {user.decode("utf-8")} ({addr}).')
                notified_socket.close()
                inputs_list.remove(notified_socket)
                del clients_list[notified_socket]
                continue

            print(f'Mensagem recebida de {user.decode("utf-8")} ({addr}): {message.decode("utf-8")}')

            for client_socket in clients_list:  #Envia a mensagem recebida para todos os outros clientes conectados no servidor
                if client_socket != notified_socket:
                    client_socket.send(user + ': '.encode('utf-8') + message + '\n'.encode('utf-8'))

    for notified_socket in exception_sockets:   #Caso o select tenha falhado na leitura de algum socket
        notified_socket.close()
        inputs_list.remove(notified_socket)
        del clients_list[notified_socket]