# -*-coding=utf-8-*-
import click
import json
import logging
from zlado.aliyun import ali_cli
from zlado import ado_ini
import os


def get_ecses():
    cfg = ado_ini.read_cfg()
    print('regions:',cfg.get('default', 'regionids').split(','))
    cli = ali_cli.AliCli(cfg.get('default', 'accesskeyid'),
                         cfg.get('default', 'accesskeysecret'),
                         cfg.get('default', 'regionids').split(','))
    return [ecs for ecs in cli.ecses_iterator()]


@click.command()
def cli():
    ecses = get_ecses()
    while True:
        os.system('clear')
        for i in range(len(ecses)):
            print(''.join([str(i+1), ':', ecses[i].__str__()]))

        indexstr=input('请选择ECS序号:')
        if not indexstr.isnumeric():
            continue
        if int(indexstr)>len(ecses):
            continue

        cur_ecs=ecses[int(indexstr)-1]
        sship = cur_ecs.ip
        # sship = '127.0.0.1'
        print('ecs',':',cur_ecs.__str__())
        os.system('ssh ' + sship)


if __name__ == '__main__':
    cli()
