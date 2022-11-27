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



def create_rb_channel_wizard(MANAGER_IP=manager_ip, START_CHANNEL_NUM=1,END_CHNNEL_NUM=100, prefix='channel', ABR_MC_ADDRESS="239.0.108.4", ABR_SOURCE='10.70.90.108' , CBR_MC_ADDRESS="239.0.106.2", CBR_SOURCE='10.70.90.106'):
    # Arguments:
    MANAGER_IP = use_default("Manager IP", MANAGER_IP)
    START_CHANNEL_NUM = use_default("First channel number", START_CHANNEL_NUM)
    END_CHNNEL_NUM = use_default("Last channel number", END_CHNNEL_NUM)
    prefix = use_default("Channel prefix", prefix)


    # Layers:
    url = 'http://'+MANAGER_IP+':5929/get_encoding_profiles?X=0'
    res = requests.get(url)
    res.encoding = 'UTF-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    names = soup.find_all('name')
    bandwidths = soup.find_all('bandwidth')
    enc_ids = soup.find_all('enc_id')
    layers = {}
    t = PrettyTable(['ID', 'Name', 'Bandwidth[Mbps]'])
    for index in range(len(names)):
        name = str(names[index].get_text())
        bandwidth = round(float(bandwidths[index].get_text()) / 1048576, 2)
        encoding_id = int(enc_ids[index].get_text())
        layers[encoding_id] = name
        t.add_row([encoding_id, name, bandwidth])
    print("The avaliable layers in this environment are:\n{}\n".format(t))


    # ABR layers:
    Y_N = ''
    while Y_N.lower() not in ['y','n']:
        Y_N = input("Do you wish to ingest ABR layers? Y/N\n")

    if Y_N.lower() == 'y':
        ABR_MC_ADDRESS = use_default("ABR multicast address", ABR_MC_ADDRESS)
        ABR_SOURCE = use_default('ABR_SOURCE', ABR_SOURCE)

        layer_list = {}
        port = 11111
        done = ''
        while done.lower() != ('c'):
            layer_id = int(input('Enter an ABR Layer ID\n'))
            while layer_id not in layers.keys():
                layer_id = int(input('Wrong ID, enter a valid ABR Layer ID\n'))
            port = use_default('Multicast Port', port)
            layer_list[layer_id] = port
            port += 1
            print('Layer added:\n{}\n'.format([layers[x] for x in layer_list.keys()]))
            done = input('Hit any key to add layer ID or (c) to continue\n')

        # ABR xml Section:
        xml_abr_layer = ''
        for id, mc_port in layer_list.items():
            xml_abr_layer += f'''
            <layers>
                <live_feed_address>{ABR_MC_ADDRESS}:{mc_port}</live_feed_address>
                <encoding_profile>{id}</encoding_profile>
            </layers>
            '''
        xml_abr = f'''
        <abr>
            <live>1</live>
            {xml_abr_layer}
            <vbr>1</vbr>
            <source_addrs>{ABR_SOURCE}:0</source_addrs>
            <edge_id>{edge_id}</edge_id>
            <live_pause>0</live_pause>
        </abr>
        '''

    else:
        ABR_MC_ADDRESS = ''
        ABR_SOURCE = ''
        layer_list = {}
        xml_abr = ''

    # CBR layer ID:
    Y_N = ''
    while Y_N.lower() not in ['y','n']:
        Y_N = input("Do you wish to ingest CBR? Y/N\n")

    if Y_N.lower() == 'y':
        CBR_MC_ADDRESS = use_default("CBR multicast address", CBR_MC_ADDRESS)
        CBR_SOURCE = use_default('CBR_SOURCE', CBR_SOURCE)
        CBR_ID = int(input("Enter CBR video profile ID\n"))
        while CBR_ID not in layers.keys():
            CBR_ID = int(input('Wrong ID, enter a valid ABR Layer ID\n'))
        CBR_ID = use_default('CBR video profile ID', CBR_ID)
        CBR_PORT = use_default('CBR Multicast port', 11111)
        LAYER_NAME = layers[CBR_ID]

        # CBR XML Section:
        xml_cbr_layer = f'''
        <cbr_sources>
            <addr>{CBR_MC_ADDRESS}:{CBR_PORT}</addr>
            <encoding_profile>{CBR_ID}</encoding_profile>
            <source_addrs>{CBR_SOURCE}:0</source_addrs>
        </cbr_sources>
        '''
        xml_cbr = f'''
                <cbr_live>1</cbr_live>
                <cbr_edge_id>{edge_id}</cbr_edge_id>
                {xml_cbr_layer}
                <cbr_live_pause>0</cbr_live_pause>
        '''
    else:
        CBR_MC_ADDRESS = ''
        CBR_SOURCE = ''
        CBR_ID = None
        CBR_PORT = ''
        LAYER_NAME = ''
        xml_cbr = ''
    
    # Summary:    
    arguments_table1 = PrettyTable(['Manager IP', 'Start Channel', 'End Channel', 'Channel Prefix'])
    arguments_table1.add_row([MANAGER_IP,START_CHANNEL_NUM,END_CHNNEL_NUM,prefix])
    print(arguments_table1)
    arguments_table2 = PrettyTable(['ABR_MC_ADDRESS','ABR_SOURCE','CBR_MC_ADDRESS','CBR_SOURCE'])
    arguments_table2.add_row([ABR_MC_ADDRESS,ABR_SOURCE,CBR_MC_ADDRESS,CBR_SOURCE])
    print(arguments_table2)
    layer_table1 = PrettyTable(['ABR Layer', 'Port'])
    for k,v in layer_list.items():
        layer_table1.add_row([layers[k],v])
    print(layer_table1)
    layer_table2 = PrettyTable(['CBR Layer', 'Port'])
    layer_table2.add_row([LAYER_NAME, CBR_PORT])
    print(layer_table2)

    # FINAL XML and POST:
    if (xml_abr and xml_cbr):
        xml_body = xml_abr + xml_cbr
    elif xml_abr:
        xml_body = xml_abr
    else:
        xml_body = xml_cbr

    xml_tail = f'''
            <specialize_compression_enable>0</specialize_compression_enable>
        </channel>
    </X>
    '''

    for IDENTITY in range(int(START_CHANNEL_NUM), int(END_CHNNEL_NUM)+1):
        CHANNEL_ID = IDENTITY
        xml_head = f'''
        <X>
            <update>0</update>
            <channel>
                <name>{prefix}_{IDENTITY}</name>
                <id>{CHANNEL_ID}</id>
                <ad_zone></ad_zone>
                <monitor>0</monitor>
                <alias></alias>
                <original_pid>0</original_pid>
        '''

        xml = xml_head + xml_body + xml_tail

        r = requests.post(f'http://{MANAGER_IP}:5929/multicast_channel/update', data=xml,
                          headers={'Content-Type': 'text/x-xml2'})
        answer = str(r)
        if answer == '<Response [200]>':
            print(f"Channel {prefix}_{IDENTITY} created")
        else:
            print(f"Failed to create {prefix}_{IDENTITY}")







create_rb_channel_wizard()
