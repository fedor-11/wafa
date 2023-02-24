import subprocess

class Network:
    def __init__(self) -> None:
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
            if (cur[0] == ''):
                cur[0] = "Untitled"
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

    def reload(self):
        subprocess.run('chcp 437', shell=True)
        self.result = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'], capture_output=True)
        self.output = self.result.stdout.decode('windows 1251')
        self.network_names = self.get_all_network_name()
        self.bssids = dict()
        for network_name in self.network_names:
            self.bssids[network_name] = self.get_bssid(network_name)


network = Network()
print(network.bssids)
