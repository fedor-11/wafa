import subprocess

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


network = Network()
print(network.bssids)
