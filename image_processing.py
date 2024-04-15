import sys

import requests
import bs4
import matplotlib

args = sys.argv

def parse_commands(user_args):
    if user_args[1] == '-c':
        count_links()
    elif user_args[1] == '-p':
        plot_data()
    elif user_args[1] == '-i':
        if user_args[3] == '-s':
            manipulate_image(user_args[3])
        elif user_args[3] == '-p':
            manipulate_image(user_args[3])
        elif user_args[3] == '-i':
            manipulate_image(user_args[3])
    else: return False

def count_links():
    pass

def plot_data():
    pass

def manipulate_image(flag):
    pass