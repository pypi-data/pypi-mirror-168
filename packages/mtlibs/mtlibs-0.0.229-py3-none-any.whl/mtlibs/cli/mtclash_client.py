#!/usr/bin/env python3

"""
搭配 `mtclash`命令使用， 让设置本容器的网关使用mtclash所提供的网络作为网络出口。
"""



import os
import sys
import subprocess
import shlex
from dotenv import load_dotenv, find_dotenv
import logging
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

load_dotenv(".env")


def main():
    logger.info("mtclash 客户端")
    gateway_ip = os.environ.get("MTX_GATEWAY_IP")
    if not gateway_ip:
        logger.error("请设置环境变量: MTX_GATEWAY_IP")
        exit(100)
        
    logger.info(f"网关IP: {gateway_ip}")
    os.system(f"ip route del default")
    os.system(f"route add default gw {gateway_ip}")
    
    logger.info("测试外网IP")
    
    
    os.system("curl --insecure ipinfo.io")
    
    logger.info("就绪")

if __name__ == "__main__":
    main()

