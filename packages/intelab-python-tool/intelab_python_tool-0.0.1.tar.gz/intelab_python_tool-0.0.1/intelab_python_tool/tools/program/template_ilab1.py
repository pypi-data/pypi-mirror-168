# -*- coding:utf-8 -*-

import os
import argparse


work_path = os.getcwd().replace("\\", "/")


def create_my_program(name: str) -> None:
    """
    创建项目框架
    :param name:
    :return:
    """
    program_path = work_path + '/' + name
    program_data_path = program_path + '/data'
    program_algorithm_path = program_path + '/algorithm'
    program_job_path = program_path + '/job'
    _create(work_path + '/README.md')
    _create(work_path + '/settings.toml')
    _create(work_path + '/setup.py')

    for _ in [program_path, program_data_path, program_algorithm_path, program_job_path]:
        os.mkdir(_)
        _create(_ + '/__init__.py')
        if _ == program_path:
            _write_main(_ + '/main.py')
        elif _ == program_data_path:
            os.mkdir(_ + '/sources')
            _create(_ + '/sources/mysql.py')
            _create(_ + '/sources/__init__.py')
            os.mkdir(_ + '/api')
            _create(_ + '/api/__init__.py')
        elif _ == program_algorithm_path:
            os.mkdir(_ + '/pretreatment')
            _create(_ + '/pretreatment/__init__.py')
            os.mkdir(_ + '/model')
            _create(_ + '/model/__init__.py')
            os.mkdir(_ + '/filter')
            _create(_ + '/filter/__init__.py')
        else:
            os.mkdir(_ + '/event')
            _create(_ + '/event/__init__.py')


def _create(name: str) -> None:
    """
    新建文件
    :param name:
    :return:
    """
    with open(name, 'w') as f:
        f.close()


def _write_main(name: str) -> None:
    with open(name, "w", encoding="utf-8") as f:
        f.write("\n")
        f.write("# Each day which without dancing is one day we betrayed of life.\n")
        f.write("# 每一个不曾起舞的日子，都是对生命最大的辜负。\n")
        f.write("\n")
        f.write("\n")
        f.write("def welcome(name='ILabor'): \n")
        f.write("    print(f'hello, {name}')\n")
        f.write("\n")
        f.write("\n")
        f.write("# It's happy to see you, now you can start your new program.\n")
        f.write("# Let's dancing algorithm with code. \n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Start Your New Program")
    parser.add_argument('-n', '--name', default='ILabProgram')
    args = parser.parse_args()
    create_my_program(args.name)

