"""Утилита ищет все файлы с именем filename во всех подкаталогах каталога catalog"""
import os
from datetime import datetime, timedelta
import re
from shutil import move
import time
import configparser
import os



def find_files(catalog, f, log=None):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        find_files += [os.path.join(root, name) for name in files if f in name and '.tmp' not in name]

    return find_files


def replace_name(lists):
    file_transfer_list=[]

    nameFileRegex = re.compile(r'(\d{7})_(\d{2})_(\d{6})_(\d{6})_(\d{1,5})')
    for row in lists:
            data_old = nameFileRegex.search(row)
            dt_data_new = datetime.strptime(str(data_old[2])+str(data_old[3]), "%y%m%d%H%M%S") + timedelta(hours=7)
            # data_new    = dt_data_new.strftime("%y-%m-%d_%H-%M-%S")
            data_new    = dt_data_new.strftime("%H-%M-%S")
            path_new = dt_data_new.strftime('\\AutoGRAPHServer_5.5\\CamPhoto\\' + data_old[0] + '\\Year_%Y\\Mon_%m\\Date_%d\\cam-'+data_old[1] + '_time_' + data_new +'.jpg')
            file_transfer_list.append([row, path_new])

    return file_transfer_list


def copy_files(copy_list, path):
    res =[]
    for row in copy_list:
        try:
            if not os.path.exists(os.path.dirname(path + row[1])):
                os.makedirs(os.path.dirname(path + row[1]))
            move(row[0],path + row[1])
        except:
             res.append(str(row) + ' - Ошибка переноса')
        else:
            res.append(str(row[0]) + ' - Перенесено успешно')

    return res


def read_config(path):
    if not os.path.exists(path):
        createConfig(path)

    config = configparser.ConfigParser()
    config.read(path)

    path_photho = config.get("Settings", "Photo")

    config.remove_option("Settings", "font_style")

    with open(path, "r") as config_file:
        config.write(config_file)


def createConfig(path):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "font", "Courier")
    config.set("Settings", "font_size", "10")
    config.set("Settings", "font_style", "Normal")
    config.set("Settings", "font_info",
               "You are using %(font)s at %(font_size)s pt")

    with open(path, "w") as config_file:
        config.write(config_file)


def main_start(path):

    lists = find_files(path, r'AGDS')
    # print(list)
    if lists:
        copy_list = replace_name(lists)
        path = ('c:')

        return copy_files(copy_list, path)


while 1:
    path = "setting.ini"
    path = (read_config(path))

    res = main_start(path)
    if res:
        print(datetime.now().strftime("%H-%M-%S") ,res)

    time.sleep(10)  # Сон

