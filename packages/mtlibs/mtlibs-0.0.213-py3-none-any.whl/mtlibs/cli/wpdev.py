#!/usr/bin/env python3

import os
import sys
import re
from version_parser import Version
from pathlib import Path
import shutil
from dotenv import load_dotenv, find_dotenv
import  argparse
from .. service.nginx import NginxService

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

load_dotenv(".env")

def main():
    """启动wordpress 开发环境"""
    NginxService().start()


if __name__ == "__main__":
    main()
