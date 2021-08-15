#!/usr/bin/env python
# -*- coding: utf-8 -*-

import quandl
from dotenv import load_dotenv
import os

load_dotenv('.env')
quandl.ApiConfig.api_key = os.getenv('QUANDL')

mydata = quandl.get_table('ZACKS/FC', ticker='AAPL')
print(mydata)
