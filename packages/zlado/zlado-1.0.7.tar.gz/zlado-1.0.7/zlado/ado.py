# -*-coding=utf-8-*-
import click
import json
import logging
from zlado.aliyun import ali_cli
from zlado import ado_ini
import os


def get_ecses():
    cfg = ado_ini.read_cfg()
    cli = ali_cli.AliCli(cfg.get('default', 'accesskeyid'),
                         cfg.get('default', 'accesskeysecret'),
                         cfg.get('default', 'regionids').split(', '))
    return [ecs for ecs in cli.ecses_iterator()]


@click.command()
def cli():
    ecses = get_ecses()
    while True:
        try:
            os.system('clear')
            for i in range(len(ecses)):
                print(i + 1, ':', ecses[i])
            index = int(input('请选择ECS序号:'))
            sship = ecses[i].ip
            # sship = '127.0.0.1'
            print('ecs',':',ecses[i].__str__())
            os.system('ssh root@' + sship)
        except:
            pass


if __name__ == '__main__':
    cli()
