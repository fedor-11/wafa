from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import backend

from .models import SSID, BSSID, Devices


def reload(request):
    data = backend.parse_from_command_line()
    print(data)
    BSSID.objects.all().delete()
    SSID.objects.all().delete()
    
    for wifi in data['all_networks'].keys():
        new_wifi = SSID(name=wifi, network=data['all_networks'][wifi]["Network"], authentication=data['all_networks'][wifi]["Authentication"], 
                        encryption=data['all_networks'][wifi]["Encryption"], is_connected=(data["connected"]==wifi))
        new_wifi.save()
        max_signal = 0
        for bssid in data['all_networks'][wifi]["BSSID"].keys():
            cur_bssid = data['all_networks'][wifi]["BSSID"][bssid]
            new_bssid = BSSID(BSSID=bssid, signal=int(cur_bssid["Signal"][:-1]), radio=cur_bssid["Radio"], band=cur_bssid["Band"], 
                              channel=cur_bssid["Channel"], SSID=new_wifi)
            new_bssid.save()
            max_signal = max(max_signal, int(cur_bssid["Signal"][:-1]))
        new_wifi.max_signal = max_signal
        new_wifi.save()
        
    return redirect("/")
            
def index(request):
    data = SSID.objects.all()
    return render(request, "main.html", {"data": data})

def wifi_details(request, wifi_name):
    ssid = SSID.objects.get(name=wifi_name)
    if (ssid.is_connected):
        st = backend.get_devices()
        all_data = 0
        for ip, size in st.items():
            all_data += size
        Devices.objects.all().delete()
        for ip, size in st.items():
            new_device = Devices(IP=ip, data_size=size, percent=(size * 100) // (all_data + 1), SSID=ssid)
            new_device.save()
        devices = Devices.objects.all()
        print(devices)
        return render(request, "wifi.html", {"wf" : wifi_name, "devices" : devices, "all_size": all_data, "is_connected" : True})
    else:
        return render(request, "wifi.html", {"wf" : wifi_name, "devices" : {}, "all_size": 0, "is_connected" : False})
