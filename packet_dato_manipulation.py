from scapy.all import *

# Les pakker fra en fil
packets = rdpcap('original.pcap')

# Endre timestampen til en bestemt dato og tid
desired_timestamp = time.mktime(time.strptime('18-10-2023 10:16:00', '%d-%m-%Y %H:%M:%S'))

for packet in packets:
    packet.time = desired_timestamp

# Lagre de endrede pakkene til en ny fil
wrpcap('modified.pcap', packets)
