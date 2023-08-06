# -*-coding=utf-8-*-

import os
import ConfigParser

ini_file = os.path.join(os.path.expanduser('~'), '.ado/config.ini')
ini_file_dir=os.path.dirname(ini_file)

if not os.path.exists(ini_file_dir):
    os.makedirs(ini_file_dir)

if not os.path.exists(ini_file):
    cfg = ConfigParser.RawConfigParser()
    cfg.add_section('config')
    # cfg.set('config','accesskeyid','')
    cfg.set('config','accesskeyid',raw_input('请输入accesskeyid:'))
    cfg.set('config','accesskeysecret',raw_input('accesskeysecret:'))
    cfg.set('config','regionids',raw_input('请输入regionids(","分隔):'))
    print('需要在配置文件中设置相应值,配置文件：',ini_file)
    f=open (ini_file,'w')
    cfg.write(f)
    f.flush()
    f.close()

def read_cfg():
    cfg = ConfigParser.RawConfigParser()
    cfg.read(ini_file)
    return cfg

