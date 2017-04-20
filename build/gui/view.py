__author__ = 'gustavosmc'
from tkinter import *
from tkinter import messagebox
import sys
import io
import qrcode
import time
import base64




sys.path.append('../')


from connection.server_connection import *
from controll.control import *
import util


BG_COLOR = "#86d7e1"
wX = 400
wY = 320

IMG_KEY = b'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'
IMG_POWER_B = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABzNJREFUeNrsWs1zU1UUP+8lTaW0TToFRhih0QWIgzYIusAFcVzIjizUjR/NBjc4Y1y4Nv4H3XTlggYdN44z6dIZP8I44wYZUmEUcUECIzB82LTQ1qZtnud37nvpy0vy3k3a0I135tKX5N17fr9zzj333HMh+r/5tKnrJ6X3sBlbBpQoafcE91jD7Fb9zQr3IveC9LMHL2wfganrY/xvhntaABuGazb1fHLvDvl04c6yi4Slni3LITTNfZLJlJ8MAQU8K8Bt0GNDfZR6diclGXBiV4Ti/LlVKz1apeKDKhWYUP7GIpX5s4vMtMzbIRGjQ/CfiRABbtDEoSHKvBhl0P1dGbH4YIUmr8xT7s9HioQiAhKfby2BqevjoiGD/VuAD1P2+EhbTXfaYJnsr3NuIkWx8NmDs5snoBZonoHHxob7aPr1PZTct6MnEaVwe5nSP92j8gJcy6pIUAggYQSAn1CaZ60/P0yTJ0Yp1h/qaeStrKxT5peHbI0Fopq4FCyR65yA0nyBTOUy0PyTbOnCPcpdY5eq1UhCcxtLmD4+n3f8vRvwxblVSv44R6mfK/LcaZtO7mGrDxEUKIpU0a+phduNh8/DbbrVfPb3JbrwYM1W0xLlX4t2RQJhlt0pxu6U56+OBlsAoZKjDRYsfL7bNnOHtW6a0uW5ywYMwMIKTdhh3IeAs0mx60Dzugu2tLhO6YuPPTObyvzSG8XgXYzRacAgljAMtUd4XMlrgazj97qhcvKvZUr8wJvRzaoHv0Ehu5tmY6zI3arKGIzVacDiWg/Z1gQUM0kPsElpRQrW5Ce/LdE8u7rhARl2EQh7fjNYBsZgbJPl2q2pYyNkpy5ptxXcFsg46YHODgvBuZsrohWlbU90MBu7u4VMZSGMheV0SAATsNmRP9OKQBq/IbfRcZs6eCYd4nGpvZEmkAq80UQA7+L3EDTKf0FCx50yR6LOWkg1ElCbVgxZZVBihsWX/WNZJnLATxzop29e3dnkQg74kMeF8O7E/n5Z2w4JzBm0sIFtbDgM2XF7r6pbIAlASImD4/syza8qPwau06zNL44ONG8whrKCWKLFfo8xGKs8Sa0JUUxAS8XrGFMeAiT5vG+eUq1RrrwibgjBIxGzJXjlQkbdCl4L1EkkBmQO8QrumBsygiKSnQAl3QQSykQR38H521V12GKJEPrB/gjF+lqD81vE9RjPYzGHKfjVGUNk+LnRaMRZyHE3gRi+DIo+hftrIsQ5Pb6/vz1h5TqG9JFI+5zxPZ7DUYjIcNIPn2hEymLxxiikcbQpLa03xPLxaPud+tTuvvoaODESbvse5jAc8QZk1Do6i4UlAvHz+GhEe5DOMe7jeKS+N3x0IBI4rVjA0oM+PtpPs/f/9c1GWy/i1Zr2u4cHQzT1Qm9Obo2pBGozzHz2YTU4sbIXrLXVKKzO5px9uNIiF9KYIT4Qcr1u0ez8+qaxYw7LkW9BhqnP2kWg4lQHfGPw7rBUDZwKyJe3qpsm8BXPYWFOR8aucGAFw8ZfchMo4hsUnXx3wX0RirIbQZxDoLLavUNh7HkQsGtb0bCS4XtUhasrkQ0ECvgSFTPfNcC7piRtlioY/MO75pnLS10T+LC4RHM8R00sagl4yAgqvdgMCh4ClpT7AnMhjizRsBIIwTN3q12ROMPgcdSsiTIsmTN7ODhq5UuLjgXyGwRUlbhSltrliv9C3hmiyZcGxOYQjKpH7tYKvX1xUcud8M47/O55TqFrthIACHNi7qBSZHlhDbJLTpnFbKhEYKIr88GHmfhTkkITg1+3ScxwDnPo+wX69Opyy+iE7/Ab3kG+s87I12vKkhO80WHOwHPI1XnHffLNCYQ6ppWQpN9490AHp7KqqMG08xnTTjMMz/2AWqgq2jhugw8AP318UKt++uzXN1Why+I8yK5ib1hAfTEN10ChVatu88ognTs2QEiJaqJRi9Z4/jX5a9la5mfLfmbA0DrexZhzLw9ogZe1d2nOLvwyRlcJvrkqwS+hSqxWO2m5U/GNqGgSoGRxC1iriQi+Hw4plymdimm5jRN56pVrT1XCaF3YMrIoJhXfeqajYi4OI/BvpMTerDLB7NB1QqW32Jv49m8qzyP+W013B0ab2uhlVMJOPzdI+Tefpu1sqe/u0syNx1g0RQavUVp0KhSWVcFAVIm3q0H2DPYmdVeQ0q9OqxibRLhAiXs7SNTL6wBvyUVHWZ/ABok0wlbu2oKYEv7Y6wYZkLUB3sr43dLoXDGN2xcd6oop2eMrpsJ93m2rbs1v4oqpcZPLS4lbrpuGpFa5pZd8l+xLvlr9ki+lc+Xa3TWr6bpmPbLJa9arnmtWqxfXrC3vEHBDr4ig3IeKGVwrPhhuSwiAS4/XxFWQVUpiRtbGDtvzi+5mIhkxNWqV5KqNGEEnwXpyVLITsyf4Xw3aL/SUXe6Lq6KT0erkXrJPUgUBrnGRHdT+E2AAwBVkirERuVAAAAAASUVORK5CYII='
IMG_POWER_B_ON = b'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'
IMG_MOBILE = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABNFJREFUeNrUWsuOFDcUvdfTDIrE0EqEQCELZoXIDhSxzgix5qH8QFiz4Q+Y+QM2rOETJlHWMKwRKMuIDQ0SSCAeIkRCwLRvfP28dpnp6q6qZrDkKld3leuc+7a7Ab7xhnPdffPRCXNcHxjTBK6efNIvgZuPLprjjSWATyQArhkif3Qn4MBv8/DE2gjW1w4Mi/z9Z3jyfjdcXppFYtRiTpY83Dp3DH4/dXgp4r/9z79w5c6L8O49Cag2Ns+SXxZ4bvyu8aqFNtNkZ2nATjCv2Wz8+aywULLHnQs/tZ7j9JGDcO/5B+hKYKE2D9CuTX3reWBuDWzefwNbD94Y6zDcFTorQXQdxHWtEaWz7WKsCa7/8j1snv1hWA1sPXhrnvLgbVepr/gux+VnquwY+9bDt8NrIIHGJPnYIddETQPkndpLHUh5zVDSUO8EJJgoNZWAK0EA5FiCD8CF2WAgEQho8U7skwDuoYE9fKGqAe6YxhI4qfydLUiMZkq+nCiCF/ZbM6WShDQdHmsd0oMHTu4zKajuBDzQUgOompqQRCL+lMiceUvJl7avc1tF/65uBFRTEog5eJWbkTLfKxSuwwdjMhZiUABhDlyHeQcxocIHMA994RpNX4kfYwIvfFeT6NGslJe+yk0IezOhwpYzm3fgVQAvSEjeIfA48AhTc8EUpzpkInQ3ZYB7JYBNx/YaCJJfiSTMmDWAeSnnCJAlgdqAV8YvzB06mg80fQChBwLlLEW0kZJf8eCViKyhRelbqRvwmp8xZ3M/ycg1vA8kAsFhpeRj5cDficDDBKY+03LY52fIPk8wtfNRU+KdCVTtMIlWiagTJM/gR0ILIX9NrReztMney2eFUsmVaNc5E2OllCiSFDbcwoEPJIL58IH8PbqR9xwhwPm3HFoWc1hRAjZKH/RBJaSJkSfAdh/MBa2Dk3/anfmaql47m0G3BQ224rq/FjRZcUOYCsyiXrNOq2UE8uWEP1N6wo+o/o5OBCiUAtTELoBL0Do6rAuRjgDFz1M5kRek2YqtPf5ZGqDmJPGNmJcGFqTLsi7agLV5GYX4nqkoJXQkVFnMtFzctNRAraanrDyQJpNCZIqjUgNMkjOwNauYqmEhEi01QDmpaMsYAXF54DKsywkuVFLTLwoyurSpxvKzkwaoKQkKCw+3CHFVvK9tNPoMSzG+BzelYDbagZ9ac6o5RN9ODDUTyrdGbJyHVNukJQTlvEk6tHQEnRyifKATAZ5AFRrQkpXXhC/lU7KCTANhRabjalLuSuxlQtSDCZXOxUYetkKs0+qYjpnA1KflkGHz5XC5maWFanShAeiJgM4nGo8Q3u166aMvHvwS11UDLnRRLA+EKVV24ySR8QEYQAOFD1z7+RDsvPhY342I5XatiKD63pAYbxxd7dkHKpLYPDNezq6tbqeBdsXcAlt+nVvLdw62vb799AOc/uul7Tzeh9Xol9vkv124fPdV9AMeP/7tR1g/1P/rBtHAhH9l5Owm+iT98rj/CbCkxyNfN5jO4yGkPxyBtRFsnz8Kvx5btZ3H/NnX8IEJH/5+9XHuiTeOfwc7pi9uhp970ID7z8Lk3ScNm/dfLy2C8rv8r/WTRZbleRN/NfgKbeZfDWb7gJvgUhtp9BnI2oDn9r8AAwBKOd6M95LCqwAAAABJRU5ErkJggg=='
IMG_SYNC = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4AEOEyw4CHwhuAAAA45JREFUSMellk1oXFUUx3/3zrxMMsyM+AFp0BQykchQ0YVF2tKF4FRJZiXpIi7sQoZASUQFF67cuBEFSciMq4ISFx0wXaVpVCpYbIykEdSCZZ7thDTWpLWm5E2czMyb946L+cqDTDLS/+7cc8/533PPuedcOAhp86H0fg7GCFPZ13GIIwTDYR/5vAOaAprLwHkgQ9uonUilzSQT2WJ89o5kbuZlq+TIbmyVHMnczEt89o4wkS2qtJk8OKK6MmUuxTKrkrPK0g5yVllimVVhylxoTVJfnMreH71yr6WzD6/nW+pGr9wTpsz7rUlS5sJ+zkVE+GJdxn4+gCRVi2Q3VNpMxjKrexql/ijIi989kMdnN4WZf4Sv7svgD1stSWKZVannRNcJxJbU3FBPg1CA9aLLUxc3Gf9lh2VL2HLA8Gv8hmb+b4czy9ue/XXMDfUgFUlVCdImpM034v2hQF/YaGwqO8LhuU3+sgGtONVt8PGzQUQLfq1I9BhMHw1RcoWn5x9QdpsUfWGDeDQUIG2OaMYGwJXhZCziubLhRYsKGkGx+FKYr4+HeLc/QAXF2WiAi8dCAPR/a5ErCsM/Wh77ZCwCLqerV+RwarA32FBatjB3uwxaMfV8kGOPNd/jJ0c6+fRIV0N+f6ATQTG3ZmPZzSgGe4PgyEldu8BgpKORDr7ZKIOhwRHGowHPyd6Ldnrk8WgAXMBQVbsaav66NUA47PMYbVcEFOBT7XcABSXXuxQJG9UqyucdjyLkV9WycKV9AoGA9i5ZebtWppqCVW7Sv3qoA2wXtCKVK3mMJle8cipXAh9gu1W7uvOyC4q7dYLL82uFZmiGInG4AyXCR2axmdDfd3jn+k5D/mmzwlu/FUCERG+AiNG80vm1Amh1tfoOtDp/7oa3zC6ciBDtUtx6pVq+ry39y2SuRIeGiVslhha3Of59Hi3gF+HCibDH/twNCzQzTcqJbDH3Zl/jsUk1bwCcWd7myzUbv1ZoBSLgiuC4wpMBxbWXH+FQp27sX8nbRD9fKfH2M52NtChDjScure8uigamj4aIP+GjYjs4jkvEJ7wQ0aSe6+LPxKP07HIOkLi0gTLU+F7ddGm/bjp6zRKmN/btti27aXMemPvOgw9+tR5iHjQn2sL/n2i3mydvZ2yqtJlkss2ZPJktqs/2nsmqjU/ACC6nceQk0B0JG1h5GxR30eoqmhnGBlr+Kv4D3VYUyxwK2H4AAAAASUVORK5CYII='



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
        photo = PhotoImage(data=base64.b64decode(IMG_KEY))
        self.lb_qrcode['image'] = photo
        self.lb_qrcode.image = photo
        self.lb_qrcode.pack(ipadx = 100 , ipady = 100)

        self.bt_reload = Button(self.layout_interfaces)
        photo_reload = PhotoImage(data=base64.b64decode(IMG_SYNC))
        self.bt_reload['image'] = photo_reload
        self.bt_reload.image = photo_reload
        self.bt_reload.pack(side = LEFT)
        self.bt_reload.bind("<Button-1>", self.reload_interfaces_lan)

        self.list = Listbox(self.layout_list)
        self.list.pack(side = TOP)

        self.lb_power = Label(self.layout)
        pi = PhotoImage(data=base64.b64decode(IMG_POWER_B))
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


        self.reload_interfaces_lan()


    def reload_interfaces_lan(self, event = None):
        if(self.server != None):
            print(self.server.closed())
        self.list.delete(0,self.list.size())
        cont = 0
        mac = MacInfo()
        interfaces = mac.get_interfaces()
        print(interfaces)
        for i in interfaces:
            self.list.insert(cont, i)
            cont+=1

    def send_message(self, event):
        if self.executor != None:
            self.executor.send_message("EXITIN", self.executor.server.clients[0].get_ip()) # TODO teste


    def init_server(self,event):
        interface = self.list.curselection()
        if len(interface) > 0:
            interface = self.list.get(interface[0])
        else:
            messagebox.showinfo("Aviso","Selecione uma interface!")
            return
        if self.server != None:
            if not self.server.closed():
                messagebox.showinfo("Aviso","Já está conectado")
                return
        ip = MacInfo().get_interface_ip(interface)
        if ip == None:
            messagebox.showinfo("Aviso","impossivel criar conexão com essa interface")
            return
        time = 20
        self.server = Server(ip)
        self.executor = Executor(self)
        self.server.set_timeout(time) #TODO tempo de espera, como configuração
        qrc = util.generate_str_connection(self.server.get_host(), self.server.get_port())
        self.show_qrcode(qrc)
        self.executor.wait_new_client()
        self.executor.start()
        self.time_thread = MainWindow.Time(self)
        self.time_thread._start(time)


    def close_server(self, event = None):
        if(self.server != None):
            self.executor.finalize_server()
            pi1 = PhotoImage(data=base64.b64decode(IMG_KEY))
            pi2 = PhotoImage(data=base64.b64decode(IMG_POWER_B))
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
        output = io.BytesIO()
        img.save(output, "GIF")
        output.seek(0)
        output_s = output.read()
        b64 = base64.b64encode(output_s).decode()
        photo = PhotoImage(data=b64)
        self.lb_qrcode['image'] = photo
        self.lb_qrcode.image = photo
        self.lb_qrcode.pack(side = LEFT)
        output.close()

    def verify(self, msg):
        if(not msg.startswith("SC")):
            return
        msg = msg[msg.find("(") + 1:msg.find(")")]
        if msg == "INITIN" :
            pi = PhotoImage(data=base64.b64decode(IMG_POWER_B_ON))
            pi2 = PhotoImage(data=base64.b64decode(IMG_MOBILE))
            self.lb_power['image'] = pi
            self.lb_power.image = pi
            self.lb_qrcode['image'] = pi2
            self.lb_qrcode.image = pi2
            self.lb_qrcode.pack(ipadx = 100, ipady = 100)
            self.time_thread.stop()
        elif msg == 'EXITIN':
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
