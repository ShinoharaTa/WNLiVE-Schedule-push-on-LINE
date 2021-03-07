#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
