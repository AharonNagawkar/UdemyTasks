#!/usr/bin/python

import requests

'''
+--------------+---------------+-------------+----------------+
|  Manager IP  | Start Channel | End Channel | Channel Prefix |
+--------------+---------------+-------------+----------------+
| 10.65.133.11 |       1       |      2      |       ch       |
+--------------+---------------+-------------+----------------+
+----------------+--------------+----------------+--------------+
| ABR_MC_ADDRESS |  ABR_SOURCE  | CBR_MC_ADDRESS |  CBR_SOURCE  |
+----------------+--------------+----------------+--------------+
|  239.0.32.12   | 10.70.90.106 |  239.0.106.2   | 10.70.90.143 |
+----------------+--------------+----------------+--------------+
+-----------+-------+
| ABR Layer |  Port |
+-----------+-------+
|    0.25   | 11111 |
|    0.6    | 11112 |
|    1.3    | 11113 |
|    2.1    | 11114 |
|    3.5    | 11115 |
|    7.0    | 11116 |
+-----------+-------+
+-----------+-------+
| CBR Layer |  Port |
+-----------+-------+
|    3.0    | 11111 |
+-----------+-------+
'''



edge_id = '27349328462'
manager_ip = '10.65.133.11'



prefix = 'Channel'
IDENTITY = 4
CHANNEL_ID = 4
ABR_MC_ADDRESS = '239.0.108.4'
ABR_SOURCE = '10.70.90.108'
CBR_MC_ADDRESS = '239.0.106.2'
CBR_SOURCE = '10.70.90.106'

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
xml_abr = f'''
        <abr>
            <live>1</live>
            <layers>
                <live_feed_address>{ABR_MC_ADDRESS}:11111</live_feed_address>
                <encoding_profile>1238627</encoding_profile>
            </layers>
            <layers>
                <live_feed_address>{ABR_MC_ADDRESS}:11112</live_feed_address>
                <encoding_profile>1238628</encoding_profile>
            </layers>
            <layers>
                <live_feed_address>{ABR_MC_ADDRESS}:11113</live_feed_address>
                <encoding_profile>1238629</encoding_profile>
            </layers>
            <layers>
                <live_feed_address>{ABR_MC_ADDRESS}:11114</live_feed_address>
                <encoding_profile>1238630</encoding_profile>
            </layers>
            <layers>
                <live_feed_address>{ABR_MC_ADDRESS}:11115</live_feed_address>
                <encoding_profile>1238631</encoding_profile>
            </layers>
            <layers>
                <live_feed_address>{ABR_MC_ADDRESS}:11116</live_feed_address>
                <encoding_profile>1238632</encoding_profile>
            </layers>
            <vbr>1</vbr>
            <source_addrs>{ABR_SOURCE}:0</source_addrs>
            <edge_id>{edge_id}</edge_id>
            <live_pause>0</live_pause>
        </abr>
'''
xml_cbr_layer = f'''
        <cbr_sources>
            <addr>{CBR_MC_ADDRESS}:11111</addr>
            <encoding_profile>451712</encoding_profile>
            <source_addrs>{CBR_SOURCE}:0</source_addrs>
        </cbr_sources>
'''
xml_cbr = f'''
        <cbr_live>1</cbr_live>
        <cbr_edge_id>{edge_id}</cbr_edge_id>
{xml_cbr_layer}
        <cbr_live_pause>0</cbr_live_pause>
'''
xml_tail = f'''
        <specialize_compression_enable>0</specialize_compression_enable>
    </channel>
</X>
'''

xml = xml_head+xml_abr+xml_cbr+xml_tail
r = requests.post(f'http://{manager_ip}:5929/multicast_channel/update', data=xml, headers={'Content-Type':'text/x-xml2'})
answer = str(r)
print(answer)
if answer == '<Response [200]>':
    print(f"Channel {prefix}_{IDENTITY} created")



#print(xml)
