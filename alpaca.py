#!/usr/bin/env python
# -*- coding: utf-8 -*-

import alpaca_trade_api
from dotenv import load_dotenv
import os
import logging

load_dotenv('.env')

# === Set Up Alpaca API ===

client_id = os.getenv('CLIENT')
secret_key = os.getenv('SECRET')
endpoint = os.getenv('ENDPOINT')

api = alpaca_trade_api.REST(client_id, secret_key, endpoint, api_version='v2')

account = api.get_account()

# =========================
# ===== Set Up Logger =====

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('tradinglog.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info('An Info Message')
logger.error('ERROR')
# =========================


def submit_simple_order(f_symbol, f_side, f_type, f_time_in_force, f_qty=None, f_notional=None, f_limit_price=None, f_stop_price=None):

    if f_type == 'market':
        if f_qty is not None:
            logger.info(
                'market %s: %s shares of %s, duration is %s', f_side, f_qty, f_symbol, f_time_in_force)
            api.submit_order(symbol=f_symbol, qty=f_qty, side=f_side,
                             type=f_type, time_in_force=f_time_in_force)
        elif f_notional is not None:
            logger.info(
                'market %s: %s worth of shares of %s, duration is %s', f_side, f_notional, f_symbol, f_time_in_force)
            api.submit_order(symbol=f_symbol, notional=f_notional, side=f_side,
                             type=f_type, time_in_force=f_time_in_force)

    elif f_type == 'limit':
        if f_qty is not None:
            logger.info(
                'limit %s: %s shares of %s, limit at %s, duration is %s', f_side, f_qty, f_symbol, f_limit_price, f_time_in_force)
            api.submit_order(symbol=f_symbol, qty=f_qty, side=f_side,
                             type=f_type, limit_price=f_limit_price, time_in_force=f_time_in_force)
        elif f_notional is not None:
            logger.info(
                'limit %s: %s worth of shares of %s, limit at %s, duration is %s', f_side, f_notional, f_symbol, f_limit_price, f_time_in_force)
            api.submit_order(symbol=f_symbol, notional=f_notional, side=f_side,
                             type=f_type, limit_price=f_limit_price, time_in_force=f_time_in_force)

    elif f_type == 'stop':
        if f_qty is not None:
            logger.info(
                'stop %s: %s shares of %s, stop at %s, duration is %s', f_side, f_qty, f_symbol, f_stop_price, f_time_in_force)
            api.submit_order(symbol=f_symbol, qty=f_qty, side=f_side,
                             type=f_type, stop_price=f_stop_price, time_in_force=f_time_in_force)
        elif f_notional is not None:
            logger.info(
                'limit %s: %s worth of shares of %s, stop at %s, duration is %s', f_side, f_notional, f_symbol, f_stop_price, f_time_in_force)
            api.submit_order(symbol=f_symbol, notional=f_notional, side=f_side,
                             type=f_type, stop_price=f_stop_price, time_in_force=f_time_in_force)

    elif f_type == 'stop_limit':
        if f_qty is not None:
            logger.info(
                'stop limit %s: %s shares of %s, stop at %s, limit at %s, duration is %s', f_side, f_qty, f_symbol, f_stop_price, f_limit_price, f_time_in_force)
            api.submit_order(symbol=f_symbol, qty=f_qty, side=f_side,
                             type=f_type, stop_price=f_stop_price, limit_price=f_limit_price, time_in_force=f_time_in_force)
        elif f_notional is not None:
            logger.info(
                'limit %s: %s worth of shares of %s, stop at %s, limit at %s, duration is %s', f_side, f_notional, f_symbol, f_stop_price, f_limit_price, f_time_in_force)
            api.submit_order(symbol=f_symbol, notional=f_notional, side=f_side,
                             type=f_type, stop_price=f_stop_price, limit_price=f_limit_price, time_in_force=f_time_in_force)

    print('order type has not been implemented')
