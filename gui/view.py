__author__ = 'gustavosmc'
from tkinter import *
import sys
import os
import qrcode
import time



sys.path.append('../img/')


from connection.server_connection import *
from controll.control import *
import util


BG_COLOR = "#86d7e1"
wX = 400
wY = 320


class MainWindow(object):
    def __init__(self, tk_instance):
        self.server = None
        self.executor = None
        tk_instance.set_window(self)
        self.time_thread = self.Time(self)


        self.main_frame = Frame(tk_instance)
        self.main_frame.pack()

        self.layout_right = LabelFrame(tk_instance)
        self.layout_right['background'] = '#289'
        self.layout_right.pack(side = RIGHT)

        self.layout = LabelFrame(self.layout_right)
        self.layout['background'] = BG_COLOR
        self.layout.pack(side = TOP)

        self.layout_interfaces = LabelFrame(self.layout_right)
        self.layout_interfaces['background'] = BG_COLOR
        self.layout_interfaces.pack(side = TOP, pady = 10)

        self.layout_list = LabelFrame(self.layout_right)
        self.layout_list['background'] = BG_COLOR
        self.layout_list.pack(side = TOP)


        self.label_time = Label(tk_instance)
        self.label_time.pack(side = BOTTOM)

        self.label_interfaces = Label(self.layout_interfaces)
        self.label_interfaces['text'] = "Interfaces"
        self.label_interfaces.pack(side = RIGHT)

        self.lb_qrcode = Label(tk_instance)
        photo = PhotoImage(file =  "../img/key.png")
        self.lb_qrcode['image'] = photo
        self.lb_qrcode.image = photo
        self.lb_qrcode.pack(ipadx = 100 , ipady = 100)

        self.bt_reload = Button(self.layout_interfaces)
        photo_reload = PhotoImage(file = '../img/button-synchronize.png')
        self.bt_reload['image'] = photo_reload
        self.bt_reload.image = photo_reload
        self.bt_reload.pack(side = LEFT)
        self.bt_reload.bind("<Button-1>", self.reload_interfaces)

        self.list = Listbox(self.layout_list)
        self.list.pack(side = TOP)

        self.lb_power = Label(self.layout)
        pi = PhotoImage(file = "../img/button-power.png")
        self.lb_power['image'] = pi
        self.lb_power.image = pi
        self.lb_power['background'] = BG_COLOR
        self.lb_power.pack(side = RIGHT)

        self.bt_init_server = Button(self.layout)
        self.bt_init_server['text'] = 'Iniciar Servidor'
        self.bt_init_server['background'] = BG_COLOR
        self.bt_init_server.bind("<Button-1>", self.init_server)
        self.bt_init_server.pack(side = TOP)

        self.bt_close_server = Button(self.layout)
        self.bt_close_server['text'] = 'Finalizar Servidor'
        self.bt_close_server['background'] = BG_COLOR
        self.bt_close_server.bind("<Button-1>", self.close_server)
        self.bt_close_server.pack(side = BOTTOM)

        self.reload_interfaces()


    def reload_interfaces(self, event = None):
        if(self.server != None):
            print(self.server.closed())
        self.list.delete(0,self.list.size())
        cont = 0
        mac = MacInfo()
        interfaces = mac.get_interfaces()
        for i in interfaces:
            self.list.insert(cont, i)
            cont+=1

    def send_message(self, event):
        print("enviando mensagem")
        if self.executor != None:
            self.executor.send_message("EXITIN", self.executor.server.clients[0].get_ip()) # TODO teste


    def init_server(self,event):
        interface = self.list.curselection()
        if len(interface) > 0:
            interface = self.list.get(interface[0])
        else:
            print("Selecione uma interface")
            return
        if self.server != None:
            if not self.server.closed():
                print("Já está conectado!")
                return
        ip = MacInfo().get_interface_ip(interface)
        if ip == None:
            print("impossivel criar conexão com essa interface")
            return
        time = 20
        self.server = Server(ip)
        self.executor = Executor(self)
        self.server.set_timeout(time) # todo tempo de espera, como configuração
        qrc = util.generate_str_connection(self.server.get_host(), self.server.get_port())
        self.show_qrcode(qrc)
        self.executor.wait_new_client()
        self.executor.start()
        self.time_thread = MainWindow.Time(self)
        self.time_thread._start(time)


    def close_server(self, event = None):
        if(self.server != None):
            self.executor.finalize_server()
            pi1 = PhotoImage(file = "../img/key.png")
            pi2 = PhotoImage(file = "../img/button-power.png")
            self.lb_qrcode['image'] = pi1
            self.lb_qrcode.image = pi1
            self.lb_power['image'] = pi2
            self.lb_power.image = pi2
            self.lb_qrcode.pack(ipadx = 100, ipady = 100)
            self.time_thread.stop()
            self.label_time['text'] = ""
            print("finalizou")


    def show_qrcode(self, str_text):
        self.lb_qrcode.pack(ipadx = 30, ipady = 30)
        img = qrcode.make(str_text, box_size = 4)
        img.save("qrcode.gif")
        photo = PhotoImage(file = "qrcode.gif")
        self.lb_qrcode['image'] = photo
        self.lb_qrcode.image = photo
        self.lb_qrcode.pack(side = LEFT)

    def verify(self, msg):
        print("entrou \o/")
        if(not msg.startswith("SC")):
            return
        msg = msg[msg.find("(") + 1:msg.find(")")]
        if msg == "INITIN" :
            print("funfou o initin")
            pi = PhotoImage(file = "../img/button-power-on.png")
            pi2 = PhotoImage(file = "../img/mobile.png")
            self.lb_power['image'] = pi
            self.lb_power.image = pi
            self.lb_qrcode['image'] = pi2
            self.lb_qrcode.image = pi2
            self.lb_qrcode.pack(ipadx = 100, ipady = 100)
            self.time_thread.stop()
        elif msg == 'EXITIN':
            print("funfou  exitin")
            self.close_server()

    class Time(Thread):
        def __init__(self, window, time = 20):

            Thread.__init__(self, name = 'time_thread')
            self.time = time
            self.window = window
            self.running = False

        def _start(self, t):
            self._stop()
            self.time = t
            self.start()


        def run(self):
            self.running = True
            while self.time > 0 and self.running:
                time.sleep(1)
                self.time -= 1
                self.window.label_time['text'] = str(self.time)
            if(not self.time > 0):
                self.window.close_server()
            self.window.label_time['text'] = ""

        def stop(self):
            self.running = False


class MyTK(Tk):
    window = None

    def set_window(self, window):
        self.window = window


    def destroy(self):
        self.window.close_server()
        Tk.destroy(self)



def main():
    root = MyTK()
    root.wm_minsize(wX, wY)
    root.wm_maxsize(wX,wY)
    root.wm_title("SMC-PC")
    MainWindow(root)
    root.mainloop()





if __name__=="__main__":
    main()