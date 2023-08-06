#!/usr/bin/env python3
import os
import sys
import subprocess
import shlex
from dotenv import load_dotenv, find_dotenv
import logging
import argparse
from ..app import app
from ..services.services import start_all_services
from mtlibs.docker_helper import isInContainer

from .sub.sub_default import command as command_default
from .sub.sub_dev import command as command_dev
from .sub.sub_deamon import command as command_deamon
from .sub.sub_mtxtun import command as command_mtxtun
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

load_dotenv(".env")

def sub_default(args):
    logger.info(f"默认入口, {args}")

def help(args):
    logger.info(f"TODO: help info.....")


def main():
    parser = argparse.ArgumentParser(description="MTXP CLI")
    # parser.add_argument('--version', action='store_true', help='show version')
    # sub help
    subparsers = parser.add_subparsers(help='子命令')
    parser_help = subparsers.add_parser('help', help='a help')
    parser_help.set_defaults(func=help)


    # # sub exec
    # # 用法：entry exec 'whoami && ls /'
    # parser_cmd = subparsers.add_parser('cmd', help='执行shell命令')
    # parser_cmd.add_argument('cmdline', help='shell 命令')
    # parser_cmd.set_defaults(func=cmd)

    # sub dev
    # 用法: ./entry install dind
    parser_dev = subparsers.add_parser('dev', help='启动开发服务器')
    # parser_dev.add_argument('package', help='包名称')
    parser_dev.set_defaults(func=command_dev)

    parser_deamon = subparsers.add_parser('deamon', help='启动相关后台服务')
    # parser_deamon.add_argument('package', help='包名称')
    parser_deamon.set_defaults(func=command_deamon)

    parser_mtxtun = subparsers.add_parser('mtxtun', help='启动mtxtun')
    parser_mtxtun.set_defaults(func=command_mtxtun)

    # # sub service
    # # 用法: ./entry service cliadmin
    # parser_cmd = subparsers.add_parser('service', help='启动服务')
    # parser_cmd.add_argument('servics', nargs='+', help='服务名称')
    # parser_cmd.set_defaults(func=service)

    # if (len(sys.argv) < 2):
    #     args = parser.parse_args(['help'])
    # else:
    #     args = parser.parse_args(sys.argv[1:])

    #设置默认函数
    parser.set_defaults(func=command_default)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
