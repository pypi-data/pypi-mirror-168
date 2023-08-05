# -*-coding=utf-8-*-

from configparser import ConfigParser
import os
ini_file = os.path.join(os.path.expanduser('~'), '.ado/config.ini')
ini_file_dir=os.path.dirname(ini_file)

if not os.path.exists(ini_file_dir):
    os.path.makedirs(ini_file_dir)

def get_ini_file():
    return ini_file

def read_cfg():
    cfg = ConfigParser()
    cfg.read(ini_file)
    return cfg

def write_cfg(cfg):
    with open (ini_file,'+w') as f:
        cfg.write(f)

def read_cfg_items(section='default'):
    cfg=read_cfg()
    if cfg.has_section(section):
        return cfg.items(section)
    else:
        cfg.add_section(section)
        write_cfg(cfg)
        return read_cfg_items(section)

def read_cfg_item(section='default',key=None):
    cfg = read_cfg()
    read_cfg_items(section)
    if cfg.has_option(section,key):
        return cfg.get(section,key)
    else:
        cfg.set(section,key,'')
        write_cfg(cfg)
        return ''

def set_default(section):
    cfg=read_cfg()
    cfg.set('default','default-section',section)
    write_cfg(cfg)

def get_default_section():
    return read_cfg_item(section='default',key='default-section')

if __name__ == '__main__':
    print(set_default('huazhu@wuhan'))
    print(read_cfg_items(section='default'))