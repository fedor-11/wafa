from scapy.all import ARP, Ether, srp

def discover_devices(ip_range):
    # Создаем ARP-запрос для указанного диапазона IP-адресов
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Отправляем пакеты и получаем ответы
    result = srp(packet, timeout=3, verbose=0)[0]

    # Обрабатываем полученные ответы
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

# Пример использования
ip_range = "192.168.29.0/24"  # Замените на ваш диапазон IP-адресов
devices = discover_devices(ip_range)

# Выводим найденные устройства
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")