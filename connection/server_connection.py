__author__ = 'gustavosmc'
import socket
from threading import *
from util import *

class Server(object):
    MAX_CONNECTIONS = 6

    def __init__(self, host='', port=7000, clients=[]):
        self.first_port = port
        self.rec_messages = []
        self.host = host
        self.port = port
        self.clients = clients
        self.init_connect()
        

    def init_connect(self):
        try:
            self.addr = (self.host, self.port)  # VARIAVEL CONTENDO OS VALORES DO IP E PORTA
            self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Especificamos os tipos: AF_INET que declara a família do protocolo; SOCKET_STREAM,indica que será TCP/IP.
            self.serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # Essa linha serve para zerar o TIME_WAIT do Socket
            self.serv_socket.bind(self.addr)  # Define para qual IP e porta o servidor deve aguardar a conexão, que no nosso caso é qualquer IP, por isso o Host é ' '.
            self.serv_socket.listen(self.MAX_CONNECTIONS)  # Define o limite de conexões.
        except OSError:
            self.port += 1
            self.init_connect()
           


        
    def set_timeout(self, time):
        self.serv_socket.settimeout(time)

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def wait_new_connection(self):
        client = Client(self)
        client.start()

    def close_server(self):
        for c in self.clients:
            self.send_message_to("EXITIN", c.get_ip())
            c.finalize_in()
            self.clients.remove(c)
        self.serv_socket.close()

    def closed(self):
        return self.serv_socket._closed

    def add_message(self, message):
        self.rec_messages.append(message)

    def recover_first_message(self):
        if (len(self.rec_messages) == 0):
            return None
        msg = self.rec_messages[0]
        self.rec_messages.remove(msg)
        return msg

    def send_message_to(self, message, ip):
        for cliente in self.clients:
            if (cliente.get_ip() == ip):
                cliente.send(message)
                break

    def add_client(self, client):
        if (self.size_clients() < self.MAX_CONNECTIONS):
            self.clients.append(client)
            return True
        return False

    def remove_client(self, ip):
        for c in self.clients:
            if (c.get_ip == ip):
                c.finalize_in()
                self.clients.remove(c)
                return True
        return False

    def contains_ip(self, ip):
        for c in self.clients:
            if (c.get_ip == ip):
                return True
        return False

    def size_clients(self):
        return len(self.clients)

    def size_messages(self):
        return len(self.rec_messages)


class Client(Thread):
    MSG_EXIT = 'SC(EXITIN)'

    def __init__(self, server):
        Thread.__init__(self)
        self.live = False
        self.server = server
        self.con = None
        self.client = None
        self.msg_send = []
        self.sendThread = self.SendThread()

    def get_ip(self):
        if (self.client != None):
            return self.client[0]
        return None

    def finalize_in(self):
        self.live = False

    def send(self, message):
        if (self.con != None):
            self.sendThread.send(self.con, message)
            return True
        return False

    def recover_first_message(self):
        if (len(self.msg_send) == 0):
            return None
        msg = self.msg_send[0]
        self.msg_send.remove(msg)
        return msg

    def run(self):
        print("Aguardando cliente")
        if (self.server.contains_ip(self.get_ip())):
            return
        try:
            self.con, self.client = self.server.serv_socket.accept()
        except Exception:
            return
        print(self.get_ip(), " se conectou ao servidor")
        self.server.add_client(self)
        msg = " "
        self.live = True
        while (self.live):
            msg = self.con.recv(1024)
            msg = str(msg, "utf-8")
            if (msg.__contains__(self.MSG_EXIT)):
                self.finalize_in()
            for s in split_comands(msg):
                if (validate_comand(s)):
                    self.server.add_message(s)
                    print(s)
        print("cliente ", self.get_ip(), " se desconectou")
        self.server.remove_client(self.get_ip())  # Quando o cliente sair ele é removido

    def get_con(self):
        return self.con

    class SendThread(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.message = str
            self.con = None

        def send(self, con, message):
            self.con = con
            self.message = message
            self.start()

        def run(self):
            self.con.send(self.message.encode())


class MacInfo(object):
    def get_host_name(self):
        return socket.gethostname()

    # Retorna o ip da interface passada como parametro, str
    def get_interface_ip(self, lan):
        import netifaces as ni
        try:
            intf = self.get_interfaces()
            ip = ni.ifaddresses(intf[intf.index(lan)])[2][0]["addr"]
            print(ip)
            return ip
        except Exception:
            return None

    # Retorna uma lista com as interfaces de rede
    def get_interfaces(self):
        import netifaces as ni
        return ni.interfaces()[2:]
