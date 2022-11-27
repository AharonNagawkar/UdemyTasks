#!/usr/bin/python


import os
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable



url = 'http://127.0.0.1:5929/get_topology?X=0'
res = requests.get(url)
res.encoding = 'UTF-8'
soup = BeautifulSoup(res.text, 'html.parser')
edge_id = str(soup.find('edges').find('id').get_text())
manager_ip = soup.find('mgr_addr').get_text().split(':')[0]


# def look_for_manager_ip():
#     manager_ip = ''
#     for root, dirs, files in os.walk('/opt/Fabrix.TV/Streamer/bin/'):
#         for name in files:
#             if name == 'streamer.ini':
#                 with open('/opt/Fabrix.TV/Streamer/bin/streamer.ini') as ini_file:
#                     data = ini_file.readlines()
#                     for line in data:
#                         if 'MANAGER_ADDRESS' in line:
#                             manager_ip = line.split('=')[1].split(':')[0]
#                             break
#
#     for root, dirs, files in os.walk('/opt/Fabrix.TV/Manager/bin/'):
#         for name in files:
#             if name == 'manager.ini':
#                 with open('/opt/Fabrix.TV/Manager/bin/manager.ini') as ini_file:
#                     data = ini_file.readlines()
#                     for line in data:
#                         if 'MANAGER_ADDR' in line:
#                             manager_ip = line.split('=')[1].split(':')[0]
#                             break
#     if not manager_ip:
#         manager_ip = input("Manager IP is not provided, please enter the environment Manager IP:\n")
#     return manager_ip

#manager_ip=look_for_manager_ip()


def use_default(name, value):
    choice = ''
    while choice.lower() != ('y' or 'n'):
        choice = input("Current value for {} is {}\nType Y/N to continue: \n".format(name, value))
        if choice.lower() == 'n':
            value = input("Enter new value for {}:\n".format(name))
    return value



def create_rb_channel_wizard(MANAGER_IP=manager_ip, START_CHANNEL_NUM=1,END_CHNNEL_NUM=100, prefix='ch', ABR_MC_ADDRESS="239.0.32.12", ABR_SOURCE='10.70.90.106' , CBR_MC_ADDRESS="239.0.106.2", CBR_SOURCE='10.70.90.143'):
    # Arguments:
    MANAGER_IP = use_default("Manager IP", MANAGER_IP)
    START_CHANNEL_NUM = use_default("First channel number", START_CHANNEL_NUM)
    END_CHNNEL_NUM = use_default("Last channel number", END_CHNNEL_NUM)
    prefix = use_default("Channel prefix", prefix)
    ABR_MC_ADDRESS = use_default("ABR multicast address", ABR_MC_ADDRESS)
    ABR_SOURCE = use_default('ABR_SOURCE', ABR_SOURCE)
    CBR_MC_ADDRESS = use_default("CBR multicast address", CBR_MC_ADDRESS)
    CBR_SOURCE = use_default('CBR_SOURCE', CBR_SOURCE)

    # Layers:
    url = 'http://10.65.133.15:5929/get_encoding_profiles?X=0'
    res = requests.get(url)
    res.encoding = 'UTF-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    names = soup.find_all('name')
    bandwidths = soup.find_all('bandwidth')
    enc_ids = soup.find_all('enc_id')
    layers = {}
    t = PrettyTable(['ID', 'Name', 'Bandwidth [Mbps]'])
    for index in range(len(names)):
        name = str(names[index].get_text())
        bandwidth = round(float(bandwidths[index].get_text()) / 1048576, 2)
        encoding_id = int(enc_ids[index].get_text())
        layers[encoding_id] = name
        t.add_row([encoding_id, name, bandwidth])
    print("The avaliable layers in this environment are:\n{}\n".format(t))

    layer_list = {}
    port = 11111
    done = ''
    while done.lower() != ('c'):
        layer_id = input('Enter a Layer ID\n')
        if layer_id not in layers.keys():
            done = raw_input('Invalid Layer ID, hit any key to add layer ID or (c) to continue\n ')
        else:
            port = use_default('Multicast Port', port)
            layer_list[layer_id] = port
            port += 1
            print('Layer added:\n{}\n'.format([layers[x] for x in layer_list.keys()]))
            done = raw_input('Hit any key to add layer ID or (c) to continue\n')

    # POD ID:
    



create_rb_channel_wizard()