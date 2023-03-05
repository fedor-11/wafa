import subprocess
import time

# класс Networks содержит всю информацию о доступных сетях
class Network:
    def __init__(self):
        self.reload()

    def get_network_name(self, start_ind):
        ind = start_ind
        while (self.output[ind] != ':'):
            ind += 1
        ind += 2
        name = ""
        while (self.output[ind] != '\r'):
            name += self.output[ind]
            ind += 1
        return [name, ind]
    
    def get_all_network_name(self):
        ind = self.output.find("\nSSID ")
        if (ind == -1):
            return ["No netwroks available"]
        names = []
        cur = ["", 0]
        while (True):
            ind = self.output.find("\nSSID ", cur[1])
            if (ind == -1):
                break
            cur = self.get_network_name(ind + 1)
            if (cur[0] != ''):
                names.append(cur[0])
        return names
    
    def get_bssid_by_index(self, start_ind):
        ind = start_ind
        while (self.output[ind] != ':'):
            ind += 1
        ind += 2
        bssid = ""
        while (self.output[ind] != '\r'):
            bssid += self.output[ind]
            ind += 1
        return [bssid, ind]
    
    def get_bssid(self, network_name):
        network_ind_in_output = self.output.find(' ' + network_name + '\r')
        network_ind = self.network_names.index(network_name)
        next_network_ind_in_output = len(self.output) - 1
        if (network_ind != len(self.network_names) - 1):
            next_network = self.network_names[network_ind + 1]
            next_network_ind_in_output = self.output.find(' ' + next_network + '\r')
        ind_bssid = self.output.find("BSSID ", network_ind_in_output, next_network_ind_in_output)
        bssids = []
        cur = [0, 0]
        while (ind_bssid != -1):
            cur = self.get_bssid_by_index(ind_bssid)
            bssids.append(cur[0])
            ind_bssid = self.output.find("BSSID ", cur[1], next_network_ind_in_output)
        return bssids

    def get_channel(self, network_name):
        network_ind_in_output = self.output.find(' ' + network_name + '\r')
           
    # делает полную перезапись всех доступных сетей
    def reload(self):
        # узнаём локализацию терминала пользователя
        tmp = subprocess.run('chcp', capture_output=True, shell=True)
        current_codepage = tmp.stdout.decode().strip().split()[-1]
        # меняем локализацию терминала на 437 (английская раскаладка)
        subprocess.run('chcp 437', shell=True)
        # получаем все доступные сети через команду 'netsh wlan show network mode=Bssid'
        self.result = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'], capture_output=True)
        # возварщаем локализацию терминала в ту, которая была у пользователя
        subprocess.run('chcp ' + str(current_codepage), shell=True)
        
        # разбираем вывод команды 'netsh wlan show network mode=Bssid'
        # декодируем, получаем строчку
        self.output = self.result.stdout.decode('windows 1251')
        # получаем список SSID всех доступных сетей
        self.network_names = self.get_all_network_name()
        # получаем BSSID всех сетей
        self.bssids = dict()
        for network_name in self.network_names:
            self.bssids[network_name] = self.get_bssid(network_name)


def parse_from_command_line() -> dict:
    output = '\r\nInterface name : Wi-Fi \r\nThere are 11 networks currently visible. \r\n\r\nSSID 1 : home36\r\n    Network type            : Infrastructure\r\n    Authentication          : WPA2-Personal\r\n    Encryption              : CCMP \r\n    BSSID 1                 : f8:f0:82:5d:b7:a2\r\n         Signal             : 24%  \r\n         Radio type         : 802.11n\r\n         Band               : 2.4 GHz\r\n         Channel            : 6 \r\n         Bss Load:\r\n             Connected Stations:         1\r\n             Channel Utilization:        8 (3 %)\r\n             Medium Available Capacity:  31250 (1000000 us/s)\r\n         Basic rates (Mbps) : 6 12 24\r\n         Other rates (Mbps) : 9 18 36 48 54\r\n\r\nSSID 2 : MX47_5G\r\n    Network type            : Infrastructure\r\n    Authentication          : WPA2-Personal\r\n    Encryption              : CCMP \r\n    BSSID 1                 : 64:64:4a:36:7f:57\r\n         Signal             : 67%  \r\n         Radio type         : 802.11ac\r\n         Band               : 5 GHz  \r\n         Channel            : 149 \r\n         Bss Load:\r\n             Connected Stations:         1\r\n             Channel Utilization:        23 (9 %)\r\n             Medium Available Capacity:  31250 (1000000 us/s)\r\n         Basic rates (Mbps) : 6 12 24\r\n         Other rates (Mbps) : 9 18 36 48 54\r\n    BSSID 2                 : 64:64:4a:36:7f:56\r\n         Signal             : 83%  \r\n         Radio type         : 802.11n\r\n         Band               : 2.4 GHz\r\n         Channel            : 11 \r\n         Bss Load:\r\n             Connected Stations:         1\r\n             Channel Utilization:        0 (0 %)\r\n             Medium Available Capacity:  31250 (1000000 us/s)\r\n         Basic rates (Mbps) : 1 2 5.5 11\r\n         Other rates (Mbps) : 6 9 12 18 24 36 48 54\r\n\r\nSSID 3 : KV-70\r\n    Network type            : Infrastructure\r\n    Authentication          : WPA2-Personal\r\n    Encryption              : CCMP \r\n    BSSID 1                 : f4:23:9c:23:2c:e8\r\n         Signal             : 38%  \r\n         Radio type         : 802.11n\r\n         Band               : 2.4 GHz\r\n         Channel            : 10 \r\n         Bss Load:\r\n             Connected Stations:         0\r\n             Channel Utilization:        30 (11 %)\r\n             Medium Available Capacity:  31250 (1000000 us/s)\r\n         Basic rates (Mbps) : 1 2 5.5 11\r\n         Other rates (Mbps) : 6 9 12 18 24 36 48 54\r\n\r\nSSID 4 : MAX\r\n    Network type            : Infrastructure\r\n    Authentication          : WPA2-Personal\r\n    Encryption              : CCMP \r\n    BSSID 1                 : 38:2c:4a:65:f0:30\r\n         Signal             : 65%  \r\n         Radio type         : 802.11g\r\n         Band               : 2.4 GHz\r\n         Channel            : 3 \r\n         Basic rates (Mbps) : 1 2 5.5 11\r\n         Other rates (Mbps) : 6 9 12 18 24 36 48 54\r\n\r\nSSID 5 : kv-35\r\n    Network type            : Infrastructure\r\n    Authentication          : WPA2-Personal\r\n    Encryption              : CCMP \r\n    BSSID 1                 : 24:d3:f2:98:68:4d\r\n         Signal             : 53%  \r\n         Radio type         : 802.11n\r\n         Band               : 2.4 GHz\r\n         Channel            : 1 \r\n         Basic rates (Mbps) : 1 2 5.5 11\r\n         Other rates (Mbps) : 6 9 12 18 24 36 48 54\r\n\r\nSSID 6 : Maxlar\r\n    Network type            : Infrastructure\r\n    Authentication          : WPA2-Personal\r\n    Encryption              : CCMP \r\n    BSSID 1                 : 24:d3:f2:bc:fb:a9\r\n         Signal             : 86%  \r\n         Radio type         : 802.11n\r\n         Band               : 2.4 GHz\r\n         Channel            : 9 \r\n         Basic rates (Mbps) : 1 2 5.5 11\r\n         Other rates (Mbps) : 6 9 12 18 24 36 48 54\r\n\r\nSSID 7 : arta\r\n    Network type            : Infrastructure\r\n    Authentication          : WPA2-Personal\r\n    Encryption              : CCMP \r\n    BSSID 1                 : 98:de:d0:6e:7e:84\r\n         Signal             : 50%  \r\n         Radio type         : 802.11n\r\n         Band               : 2.4 GHz\r\n         Channel            : 7 \r\n         Basic rates (Mbps) : 1 2 5.5 11\r\n         Other rates (Mbps) : 6 9 12 18 24 36 48 54\r\n\r\nSSID 8 : MaxnetX47_5  Channel Utilization:        0 (0 %)\r\n             Medium Available Capacity:  31250 (1000000 us/s)\r\n         Basic rates (Mbps) : 1 2 5.5 11\r\n         Other rates (Mbps) : 6 9 12 18 24 36 48 54\r\n\r\n'
    output = output.split('\r\n')
    # удаляем лишнии строчки в начале
    output = output[4:]
    # сюда всё будет складываться
    data = dict()
    # путь в словаре
    current_path = []
    # если какой-то параметр пустой, то нужно пропускать строчки, которые под этим параметром
    is_skip = False
    # глубина строчки на которой нужно прекратить выкидывать строчки
    should_stop_on = 0
    
    # перебираем всё строчке в выводе
    for line in output:
        # получаем количество пробелов в начале текущей строки
        amount_current_spaces = 0
        while (amount_current_spaces < len(line) and line[amount_current_spaces] == ' '):
            amount_current_spaces += 1
        # проверка на корректность данной строки
        # проверка линии у ктоторых глубина > 9 нам не нужны
        # а также если вся строка из пробелов нам не подходит
        if (amount_current_spaces > 9 or amount_current_spaces == len(line)):
            continue
            
        tp = ''
        value = ''
        line = line.strip()
        ind = 0
        # находим тип
        while (line[ind] != ' '):
            tp += line[ind]
            ind += 1
        # ищем начало значения
        while (ind < len(line) and line[ind] != ':'):
            ind += 1
        # если нет :
        if (ind == len(line)):
            continue
        # += 2 так как там ": " и потом начинает название
        ind += 2
        # получаем значение
        while (ind < len(line)):
            value += line[ind]
            ind += 1
        # если это левая строка    
        if (tp == 'SSID' and value.find("Channel Utilization:") != -1):
            is_skip = True
            should_stop_on = 0
            continue
        # проверка на то, что данную строчку нужно пропускать или нет
        if (is_skip and amount_current_spaces != should_stop_on):
            continue
        else:
            # если не нужно то заканчиваем пропускать
            is_skip = False
        # если значение пустое, то оно нам не подходит и надо начинать пропускать строчки до следующего значения
        # на уровне с этим
        if (value == ''):
            is_skip = True
            should_stop_on = amount_current_spaces
            continue
        
        # теперь разбор случаем на глубину значения
        if (amount_current_spaces == 0): # это просто нзвание сети
            data[value] = dict()
            current_path = [value]
        elif (amount_current_spaces == 4): # первичные параметры внутри сети
            if (tp == 'BSSID'):
                while (len(current_path) < 3):
                    current_path.append('')
                current_path[1] = tp
                current_path[2] = value
                if (tp not in list(data[current_path[0]].keys())):
                    data[current_path[0]][current_path[1]] = dict()
                data[current_path[0]][current_path[1]][current_path[2]] = dict()
            else:
                data[current_path[0]][tp] = value    
        elif (amount_current_spaces == 9): # параметры внутри BSSID
            data[current_path[0]][current_path[1]][current_path[2]][tp] = value
        # перезаписываем количество пробелов в предыдущей строке
    return data

if __name__ == "__main__":
    #network = Network()
    #print(network.bssids)
    while (True):
        time.sleep(60)
        try:
            parse_from_command_line()
        except:
            print("Error")
            tmp = subprocess.run('chcp', capture_output=True, shell=True)
            current_codepage = tmp.stdout.decode().strip().split()[-1]
            subprocess.run('chcp 437', shell=True)
            result = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'], capture_output=True)
            subprocess.run('chcp ' + str(current_codepage), shell=True)
            output = result.stdout
            print(output)
            print("\n\n\n\n")
            break
