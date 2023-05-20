from scapy.all import *
from scapy.layers.http import HTTP
from scapy.layers.http import HTTPRequest

st = dict()


def packet_handler(packet):
    # Извлекаем информацию о источнике, получателе и размере пакета
    if (TCP not in packet) or (IP not in packet):
        return
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    size = len(packet)

    # Выводим информацию в консоль
    # print(f"Отправитель: {src_ip} | Получатель: {dst_ip} | Размер: {size} байт")
    # print(classify_device(packet))
    if (src_ip not in st.keys()):
        st[src_ip] = size
    else:
        st[src_ip] += size

sniff(iface="Wi-Fi", prn=packet_handler, timeout=10)
print(st)
