import subprocess

# 1.1
def parse_from_command_line() -> dict:
    # узнаём локализацию терминала пользователя
    # tmp = subprocess.run('chcp', capture_output=True, shell=True)
    # current_codepage = tmp.stdout.decode().strip().split()[-1]
    # меняем локализацию терминала на 437 (английская раскаладка)
    subprocess.run('chcp 437', shell=True)
    # получаем сеть к которой сейчас подключены
    output = subprocess.check_output(['netsh', 'wlan', 'show', 'interface'])
    output_str = output.decode('windows 1251')
    ssid_start = output_str.find('SSID')
    ssid_connected = "Untiteld11"
    if (ssid_start != -1):
        ssid_end = output_str.find('\n', ssid_start)
        ssid_connected = output_str[ssid_start: ssid_end].split(':')[1].strip()
    # получаем все доступные сети через команду 'netsh wlan show network mode=Bssid'
    result = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'], capture_output=True)
    # возварщаем локализацию терминала в ту, которая была у пользователя
    # subprocess.run('chcp ' + str(current_codepage), shell=True)
    # разбираем вывод команды 'netsh wlan show network mode=Bssid'
    # декодируем, получаем строчку
    output = result.stdout.decode('windows 1251')
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
    nw_data = dict()
    nw_data['all_networks'] = data
    nw_data['connected'] = ssid_connected
    # возвращаем словарь
    return nw_data

if __name__ == "__main__":
    print(parse_from_command_line())
