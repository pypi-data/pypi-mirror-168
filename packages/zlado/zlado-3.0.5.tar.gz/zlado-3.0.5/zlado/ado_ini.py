# -*-coding=utf-8-*-

import os
from configparser import ConfigParser

ini_file = os.path.join(os.path.expanduser('~'), '.ado/config.ini')
ini_file_dir=os.path.dirname(ini_file)

if not os.path.exists(ini_file_dir):
    os.makedirs(ini_file_dir)

if not os.path.exists(ini_file):
    cfg = ConfigParser()
    cfg.add_section('config')
    # cfg.set('config','accesskeyid','')
    cfg.set('config','accesskeyid',input('请输入accesskeyid:'))
    cfg.set('config','accesskeysecret',input('accesskeysecret:'))
    cfg.set('config','regionids',input('请输入regionids(","分隔):'))
    print('需要在配置文件中设置相应值,配置文件：',ini_file)
    with open (ini_file,'+w') as f:
        cfg.write(f)

def read_cfg():
    cfg = ConfigParser()
    cfg.read(ini_file)
    return cfg

