__author__ = 'gustavosmc'
from threading import Thread
import pyautogui
from util import *

pyautogui.PAUSE = 0.001
pyautogui.FAILSAFE = False

SERVER_COMAND = "SC"

DOWN_KEY = "DK"
UP_KEY = "UK"
CLICK_KEY = "CK"
CLICK_MOUSE = "CM"

MOVE_MOUSE = "MM"
DEFINE_MOUSE = "RM"
DOWN_MOUSE = "DM"
UP_MOUSE = "UM"
CLICK_MOUSE = "CM"
LONG_MOUSE = "LM"

LEFT_SEPARATOR = "("
CENTER_SEPARATOR = ","
RIGHT_SEPARATOR = ")"

class GComand(object):


    def execute_comand(self, comand):
        if(not validate_comand(comand)):
            return
        str_com = comand[comand.find(' ') + 1: comand.find(LEFT_SEPARATOR)]
        str_valor = comand[comand.find(LEFT_SEPARATOR) + 1:comand.find(RIGHT_SEPARATOR)]
        if str_com == DOWN_KEY:
            self.down_key_comand(str_valor)
        elif str_com == UP_KEY:
            self.up_key_comand(str_valor)
        elif str_com == CLICK_KEY:
            self.click_comand(str_valor)
        elif str_com == MOVE_MOUSE:
            self.move_mouse(str_valor)
        elif str_com == DEFINE_MOUSE:
            self.define_mouse(str_valor)
        elif str_com == CLICK_MOUSE:
            self.click_mouse(str_valor)
        elif str_com == LONG_MOUSE:
            self.long_mouse(str_valor)



    def click_comand(self, key):
        pyautogui.press(key)

    def down_key_comand(self, key):
        pyautogui.keyDown(key)

    def up_key_comand(self, key):
        pyautogui.keyUp(key)

    def move_mouse(self, position):
        x, y = position.split(',')
        x, y = int(x), int(y)
        pyautogui.moveRel(x,y)

    def define_mouse(self, position):
        x, y = position.split(',')
        x, y = int(x), int(y)
        pyautogui.moveTo(x, y)

    def click_mouse(self, key):
        pyautogui.click(pyautogui.position()[0], pyautogui.position()[1], button=key)

    def long_mouse(self, key):
        pyautogui.mouseDown(pyautogui.position()[0], pyautogui.position()[1], button=key)


class Executor(Thread):
    def __init__(self, window , gcomand = GComand()):
        Thread.__init__(self)
        self.window = window
        self.server = window.server
        self.gcomand = gcomand
        self.running = True

    def finalize_server(self):
        self.running = False
        self.server.close_server()

    def send_message(self, message, ip_client):
        self.server.send_message_to(message, ip_client)

    def finalize_client(self, ip):
        self.server.remove_client(ip)

    def wait_new_client(self):
        self.server.wait_new_connection()


    # TODO aprimorar metodo
    def run(self):
        self.running = True
        while(self.running):
           msg = self.server.recover_first_message()
           if(msg != None):
                   self.window.verify(msg)
                   self.gcomand.execute_comand(msg)


