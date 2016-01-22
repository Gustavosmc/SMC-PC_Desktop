__author__ = 'gustavosmc'
import socket

host = '192.168.1.8' #IP DA MÁQUINA ATUAL
port = 7000 #PORTA QUE SERÁ UTILIZADA PARA CONEXÃO
recebe = "" #Variável que recebera a mensagem
addr = (host, port) #VARIAVEL CONTENDO OS VALORES DO IP E PORTA
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Especificamos os tipos: AF_INET que declara a família do protocolo; SOCKET_STREAM, indica que será TCP/IP.
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Essa linha serve para zerar o TIME_WAIT do Socket
serv_socket.bind(addr) #Define para qual IP e porta o servidor deve aguardar a conexão, que no nosso caso é qualquer IP, por isso o Host é ' '.
serv_socket.listen(10) #Define o limite de conexões.

print('Aguardando conexao...')
con, cliente = serv_socket.accept() #Tupla contendo dois valores, número da conexão e endereço IP do cliente.
print('Conectado')
print('aguardando mensagem')
print(cliente[0].__class__, cliente[0])
while(recebe != "QSAIR"): #Enquanto a mensagem recebida for diferente de QSAIR o programa continuará recebendo mensagens.
    recebe = con.recv(1024) #Aguarda um dado enviado pela rede de até 1024 Bytes
    recebe = str(recebe, 'utf-8')
    con.send(recebe.encode())
    print('Mensagem recebida: '+ recebe + " - IP: " + str(cliente[0]) )

serv_socket.close() #Encerra a conexão
