# -*-coding=utf-8-*-
import click
import json
import logging
from zlado.aliyun import ali_cli
from zlado import ado_ini
import os


def get_ecses():
    cfg = ado_ini.read_cfg()
    print('regions:',cfg.get('config', 'regionids').split(','))
    cli = ali_cli.AliCli(cfg.get('config', 'accesskeyid'),
                         cfg.get('config', 'accesskeysecret'),
                         cfg.get('config', 'regionids').split(','))
    ecses= [ecs for ecs in cli.ecses_iterator()]
    ecses = sorted(ecses, key=lambda x: x.hostname, reverse=False)
    return ecses.sort()


@click.command()
def cli():
    ecses = get_ecses()
    while True:
        try:
            os.system('clear')
            for i in range(len(ecses)):
                print(''.join([str(i + 1), ' :', ecses[i].__str__()]))

            indexstr = input('请选择ECS序号:')
            if not isinstance(indexstr, int):
                continue
            if int(indexstr) > len(ecses):
                continue

            cur_ecs = ecses[int(indexstr) - 1]
            sship = cur_ecs.ip
            # sship = '127.0.0.1'
            print('ecs', ':', cur_ecs.__str__())
            os.system('ssh ' + sship)
        except SyntaxError as e:
            pass


if __name__ == '__main__':
    cli()
