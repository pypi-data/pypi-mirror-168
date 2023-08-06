#!/use/bin/env python3
import sys
from pathlib import Path
from os.path import join
from dotenv import load_dotenv, find_dotenv
import logging
from flask import Flask
import click
from flask import Flask
from flask.cli import FlaskGroup
from mtxp.config import config  # 导入存储配置的字典
from werkzeug.serving import is_running_from_reloader
import argparse
from urllib.parse import urlparse
from mtlibs.docker_helper import isInContainer

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
data_dir = join(Path(__file__).parent, "data")

def create_app():
    app = Flask('mtxpagent')
    app.config.from_object(config['development'])  # 获取相应的配置类
    # from admin import admin_blue
    # from user import user_blue

    # app.register_blueprint(admin_blue)
    # app.register_blueprint(user_blue)

    from .mtxp import mtxp_blue
    app.register_blueprint(mtxp_blue)


    from mtxp.contentful import contentful_blue
    app.register_blueprint(contentful_blue)

    return app

app = create_app()

# API_PREFIX = app.config.get("API_PREFIX", "/mtpapi")



# @app.before_first_request
# def activate_job():
#     """
#         当接收到第一个请求时，触发本定时任务。
#     """
#     logger.info("activate_job called.....")
#     def run_job():
#         while True:
#             logger.info("执行后台任务...")
#             time.sleep(3)
#     thread = threading.Thread(target=run_job)
#     thread.start()

@click.command()
def cli():
    logger.info("cli command")
    print("cli command")


@click.group(cls=FlaskGroup, create_app=create_app)
def cli2():
    print("cli111 callled")
    """Management script for the Wiki application."""

# # @app.cli.command("hello_command")
# # @click.argument("ccurl")
# # @with_appcontext
# def entry_agent():
#     """本地代理入口"""
#     ccurl = sys.argv[1]
#     if ccurl:
#         logger.info(f" 启动参数: {sys.argv} ")
#         logger.info(f"ccurl : {ccurl}")
#         logger.info(f"作为agent运行")
#         def initAgent():
#             config_url = f"{ccurl}/mtxp/tun_config"
#             logger.info(f"config_url {config_url}")
#             x = requests.get(config_url)
#             jsonData= x.json()
#             logger.info(f"配置数据 {jsonData}")
#             # logger.info(f"启动端口转发")
#             pf_items = jsonData["data"]["pf"]["items"]
#             for item in pf_items:
#                 logger.info(f"(TODO)启动一个端口转发 {item}")
#                 # startup_pf(item["rhost"],item["rport"],item["lhost"], item["lport"])

#         initAgent()
#         app.run(debug=True, host='0.0.0.0', port=5500)


def entry_agent(args):
    logger.info(f"entry_agent {args}")
    # ccurl = args.url
    # logger.info(f"ccurl : {ccurl}")

    uri = urlparse(args.url)
    logger.info(f" ccuri: {uri}")
    app.run(debug=True, host='0.0.0.0', port=5500)

# def subcommand_start(args):
#     from .services.services import start_all_services

#     if not is_running_from_reloader():
#         if isInContainer():
#             start_all_services()

#     app.run(debug=True, host='0.0.0.0', port=5000)

def main():
    parser = argparse.ArgumentParser(description="mtxp")
    subparsers = parser.add_subparsers(help="mtxp")

    # sub agent
    sub_agent = subparsers.add_parser('agent', help='mtxp agent')
    sub_agent.set_defaults(func=entry_agent)
    sub_agent.add_argument('--url')

    # sub start
    # sub_start = subparsers.add_parser('start', help='start the service')
    # sub_start.set_defaults(func=subcommand_start)

    # if (len(sys.argv) < 2):
    #     args = parser.parse_args(['start'])
    # else:
    #     args = parser.parse_args(sys.argv[1:])

    args = parser.parse_args()

    # print(args)
    # init_global()
    # init_by_env()
    # init_args(args)
    args.func(args)
    # args.func(args)

if __name__ == "__main__":
    main()
