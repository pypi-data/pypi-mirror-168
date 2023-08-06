import codecs
import getpass
import json
import pickle

import numpy as np
import pandas as pd
import requests
from smartapi import SmartConnect
from smartapi import SmartWebSocket

from retrying import retry
from quantplay.broker.generics.broker import Broker
from quantplay.config.qplay_config import QplayConfig
from quantplay.model.exchange.instrument import QuantplayInstrument
from quantplay.utils.constant import Constants
from quantplay.exception.exceptions import InvalidArgumentException
from quantplay.utils.exchange import Market as MarketConstants

class AngelOne(Broker):
    angelone_api_key = "angelone_api_key"
    angelone_api_secret = "angelone_api_secret"
    angelone_client_id = "angelone_client_id"
    angelone_wrapper = "angelone_wrapper"
    angel_refresh_token = "angel_refresh_token"

    def __init__(self):
        try:
            wrapper = QplayConfig.get_value(AngelOne.angelone_wrapper)
            self.wrapper = pickle.loads(codecs.decode(wrapper.encode(), "base64"))
            self.refreshToken = QplayConfig.get_value(AngelOne.angel_refresh_token)
            user_profile_response = self.wrapper.getProfile(self.refreshToken)
            if user_profile_response['message'] != "SUCCESS":
                raise Exception("AngelOne Token Expired")
            else:
                Constants.logger.info(user_profile_response)
        except Exception as e:
            Constants.logger.error(e)
            self.wrapper = self.generate_token()
            Constants.logger.info(self.wrapper.getProfile(self.refreshToken))
        self.refreshToken = QplayConfig.get_value(AngelOne.angel_refresh_token)
        self.client_id = QplayConfig.get_value(AngelOne.angelone_client_id)

        self.angelone_ws = SmartWebSocket(self.wrapper.getfeedToken(), self.client_id)

        super(AngelOne, self).__init__()
        self.populate_instruments()

    def get_symbol_token(self, exchange, tradingsymbol):
        return self.exchange_symbol_to_instrument_id_map[exchange][tradingsymbol]

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def get_ltp(self, exchange=None, tradingsymbol=None):
        if tradingsymbol in MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP:
            tradingsymbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[tradingsymbol]

        symboltoken = self.get_symbol_token(exchange, tradingsymbol)

        if exchange == "NSE" and tradingsymbol not in ["NIFTY", "BANKNIFTY"]:
            tradingsymbol = "{}-EQ".format(tradingsymbol)

        response = self.wrapper.ltpData(exchange, tradingsymbol, symboltoken)
        if 'status' in response and response['status'] == False:
            raise InvalidArgumentException("Failed to fetch ltp broker error {}".format(response))

        return response['data']['ltp']

    def place_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                    tag=None, product=None, price=None, trigger_price=None):
        order = {}
        order["transactiontype"] = transaction_type

        order["variety"] = "NORMAL"
        order["tradingsymbol"] = tradingsymbol
        if order_type == "SL":
            order["variety"] = "STOPLOSS"

        if exchange == "NSE":
            order["tradingsymbol"] = "{}-EQ".format(tradingsymbol)

        order["triggerprice"] = trigger_price
        order["exchange"] = exchange
        order['symboltoken'] = self.get_symbol_token(exchange, tradingsymbol)

        if order_type == "SL":
            order_type = "STOPLOSS_LIMIT"
        order['ordertype'] = order_type

        if product == "MIS":
            product = "INTRADAY"
        elif product == "NRML":
            product = "CARRYFORWARD"
        order['producttype'] = product

        order['price'] = price
        order['quantity'] = quantity
        order["duration"] = "DAY"

        try:
            print("Placing order {}".format(json.dumps(order)))
            return self.wrapper.placeOrder(order)
        except Exception as e:
            exception_message = "Order placement failed with error [{}]".format(str(e))
            print(exception_message)


    def populate_instruments(self):
        Constants.logger.info("Setting up AngelOne client")
        data = requests.get("https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json")
        inst_data = json.loads(data.content)
        inst_data = pd.DataFrame(inst_data)
        inst_data.loc[:, 'exchange'] = inst_data.exch_seg
        inst_data = inst_data[inst_data.exchange.isin(["NSE", "NFO"])]
        inst_data.loc[:, 'instrument_token'] = inst_data.token.astype(int)
        inst_data.loc[:, 'symbol'] = inst_data['symbol'].str.replace('-EQ','')

        assert set(['OPTSTK', 'OPTIDX', 'FUTSTK', 'FUTIDX']) == set(inst_data[inst_data.exch_seg == "NFO"].instrumenttype.unique())

        inst_data.loc[:, 'segment'] = None
        inst_data.loc[:, 'segment'] = np.where((inst_data.exch_seg == "NFO") & (
                    (inst_data.instrumenttype == "OPTIDX") | (inst_data.instrumenttype == "OPTSTK")),
                                               "NFO-OPT", inst_data.segment)
        inst_data.loc[:, 'segment'] = np.where((inst_data.exch_seg == "NFO") & (
                    (inst_data.instrumenttype == "FUTIDX") | (inst_data.instrumenttype == "FUTSTK")),
                                               "NFO-FUT", inst_data.segment)
        inst_data.loc[:, 'segment'] = np.where(inst_data.exch_seg == "NSE",
                                               "NSE", inst_data.segment)
        inst_data = inst_data[~inst_data.segment.isna()]
        inst_data.loc[:, 'instrument_type'] = np.where(inst_data.segment == "NFO-FUT", "FUT", None)
        inst_data.loc[:, 'instrument_type'] = np.where(inst_data.segment == "NSE", "EQ",
                                                       inst_data.instrument_type)
        inst_data.loc[:, 'instrument_type'] = np.where(
            ((inst_data.segment == "NFO-OPT") & (inst_data.symbol.str[-2:] == "PE")),
            "PE", inst_data.instrument_type)
        inst_data.loc[:, 'instrument_type'] = np.where(
            ((inst_data.segment == "NFO-OPT") & (inst_data.symbol.str[-2:] == "CE")),
            "CE", inst_data.instrument_type)
        inst_data.to_csv('/tmp/inst_data.csv')
        inst_data = inst_data.to_dict('records')

        instruments = list(
            map(
                lambda z_instrument: QuantplayInstrument.from_angelone_instrument(
                    z_instrument
                ),
                inst_data,
            )
        )
        self.instruments = instruments

        Broker.populate_instruments(self, instruments)


    def configure(self):
        quantplay_config = QplayConfig.get_config()

        print("Enter AngelOne API key:")
        api_key = input()

        print("Enter AngelOne API Secret:")
        api_secret = input()

        print("Enter AngelOne Client ID:")
        client_id = input()

        quantplay_config['DEFAULT'][AngelOne.angelone_api_key] = api_key
        quantplay_config['DEFAULT'][AngelOne.angelone_api_secret] = api_secret
        quantplay_config['DEFAULT'][AngelOne.angelone_client_id] = client_id

        with open('{}/config'.format(QplayConfig.config_path), 'w') as configfile:
            quantplay_config.write(configfile)

    def validate_config(self, quantplay_config):
        if quantplay_config is None:
            return False
        if AngelOne.angelone_api_key not in quantplay_config['DEFAULT']:
            return False
        if AngelOne.angelone_api_secret not in quantplay_config["DEFAULT"]:
            return False
        if AngelOne.angelone_client_id not in quantplay_config["DEFAULT"]:
            return False

        return True

    def option_symbol(self, underlying_symbol, expiry_date, strike_price, type):
        option_symbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[underlying_symbol]
        option_symbol += expiry_date.strftime("%d")
        option_symbol += expiry_date.strftime("%b").upper()
        option_symbol += expiry_date.strftime('%y')

        option_symbol += str(int(strike_price))
        option_symbol += type

        return option_symbol

    def generate_token(self):
        quantplay_config = QplayConfig.get_config()

        if not self.validate_config(quantplay_config):
            self.configure()
            quantplay_config = QplayConfig.get_config()
        api_key = quantplay_config['DEFAULT'][AngelOne.angelone_api_key]
        api_secret = quantplay_config['DEFAULT'][AngelOne.angelone_api_secret]
        client_id = quantplay_config['DEFAULT'][AngelOne.angelone_client_id]
        wrapper = SmartConnect(api_key=api_key)

        password = getpass.getpass()
        data = wrapper.generateSession(client_id, password)

        if 'message' in data and 'status' in data and data['status'] == False:
            print(data['message'])
            raise Exception("Token generation Failed")

        self.refreshToken = data['data']['refreshToken']
        QplayConfig.save_config(AngelOne.angel_refresh_token, self.refreshToken)

        QplayConfig.save_config("angelone_wrapper", codecs.encode(pickle.dumps(wrapper), "base64").decode())
        return wrapper