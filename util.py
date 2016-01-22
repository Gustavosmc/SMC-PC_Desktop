__author__ = 'gustavosmc'
import re

rex = re.compile(' {0,1}\w{2}\((-|\w|,)+\)')

def validate_comand(command):
    if(rex.match(command) != None):
        return True
    return False

def generate_str_connection(host, port,  pass_key = "smcpcpass"):
    return '('+host+','+str(port)+','+pass_key+')'


def split_comands(str_comands):
    return str_comands.split(" ");