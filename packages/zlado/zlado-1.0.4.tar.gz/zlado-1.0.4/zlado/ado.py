# -*-coding=utf-8-*-
import click
import json
import logging
from zlado.aliyun import ali_cli
from zlado import ado_ini


@click.group()
def cli():
    pass


@cli.command()
def show():
    print('ini_file', ':', ado_ini.get_ini_file())
    print('workspaces: \n', ','.join(filter(lambda item: item != 'default', ado_ini.read_cfg().sections())))


@cli.command()
@click.option('--section', '-s', default=None, help='设置当前工作空间')
def default(section):
    if section:
        ado_ini.set_default(section)
    default_section = ado_ini.get_default_section()
    print('default_section', ':', default_section, '\n')
    for k, v in ado_ini.read_cfg_items(default_section):
        print(k, ':', v)


@cli.command()
def ecs():
    for ecs in ali_cli.get_default_ecs():
        print(ecs)

ecsip=list(map(lambda ecs:ecs.ip,ali_cli.get_default_ecs()))

import os
@cli.command()
def ssh():
    while True:
        for i in range(len(ali_cli.get_default_ecs())):
            print(i+1,':',ali_cli.get_default_ecs()[i])
        index=int(input('ecs input:'))
        sship=ali_cli.get_default_ecs()[i].ip
        sship='127.0.0.1'
        os.system('ssh shimei@'+sship)



if __name__ == '__main__':
    cli()
