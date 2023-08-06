import pandas as pd
import codecs
import pickle
import numpy as np
import time
from retrying import retry
from quantplay.utils.constant import Constants
from quantplay.exception.exceptions import InvalidArgumentException
from quantplay.broker.generics.broker import Broker
from quantplay.config.qplay_config import QplayConfig
from kiteconnect import KiteConnect
import traceback
from quantplay.broker.kite_utils import KiteUtils
from quantplay.utils.exchange import Market as MarketConstants
from datetime import timedelta

class Zerodha(Broker):

    stoploss = 'stoploss'
    zerodha_api_key = "zerodha_api_key"
    zerodha_api_secret = "zerodha_api_secret"
    zerodha_wrapper = "zerodha_wrapper"

    def __init__(self):
        try:
            wrapper = QplayConfig.get_value(Zerodha.zerodha_wrapper)
            self.set_wrapper(wrapper)
            self.wrapper.orders()
        except Exception as e:
            self.wrapper = self.generate_token()
        Constants.logger.info(self.wrapper.profile())

        super(Zerodha, self).__init__()

    def set_wrapper(self, serialized_wrapper):
        self.wrapper = pickle.loads(codecs.decode(serialized_wrapper.encode(), "base64"))

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def get_ltp(self, exchange=None, tradingsymbol=None):
        try:
            key = "{}:".format(exchange) + tradingsymbol
            response = self.wrapper.ltp([key])

            if key not in response:
                raise InvalidArgumentException("Symbol {} not listed on exchange".format(tradingsymbol))

            response = response[key]['last_price']
            return response
        except Exception as e:
            exception_message = "GetLtp call failed for [{}] with error [{}]".format(tradingsymbol, str(e))
            Constants.logger.error("{}".format(exception_message))

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def get_orders(self):
        return self.wrapper.orders()



    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def modify_order(self, data):
        try:
            response = self.wrapper.modify_order(order_id=data['order_id'],
                                              variety=data['variety'],
                                              price=data['price'],
                                              trigger_price=data['trigger_price'],
                                              order_type=data['order_type'])
            return response
        except Exception as e:
            exception_message = "OrderModificationFailed for {} failed with exception {}".format(data['order_id'], e)
            Constants.logger.error("{}".format(exception_message))

    def get_ltp_by_order(self, order):
        exchange = order['exchange']
        tradingsymbol = order['tradingsymbol']

        return self.get_ltp(exchange, tradingsymbol)

    def modify_orders_till_complete(self, orders_placed):
        modification_count = {}
        while 1:
            time.sleep(10)
            orders = pd.DataFrame(self.get_orders())

            orders = orders[orders.order_id.isin(orders_placed)]
            orders = orders[~orders.status.isin(["REJECTED", "CANCELLED", "COMPLETE"])]

            if len(orders) == 0:
                Constants.logger.info("{} ALL orders have be completed".format(self.get_username()))
                break

            orders = orders.to_dict('records')
            for order in orders:
                order_id = order['order_id']

                ltp = self.get_ltp_by_order(order)
                order['price'] = ltp
                self.modify_order(order)

                if order_id not in modification_count:
                    modification_count[order_id] = 1
                else:
                    modification_count[order_id] += 1

                time.sleep(.1)

                if modification_count[order_id] > 5:
                    order['order_type'] = "MARKET"
                    order['price'] = 0
                    Constants.logger.info("Placing MARKET order [{}]".format(order))
                    self.modify_order(order)

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def get_positions(self):
        return self.wrapper.positions()

    def positions_pnl(self):
        positions = pd.DataFrame(self.get_positions()['net'])
        Constants.logger.info("{} Total PnL {}".format(self.username, positions.pnl.astype(float).sum()))

    def close_intraday_positions(self, tag="ALL"):
        orders = pd.DataFrame(self.get_orders())

        if len(orders) == 0:
            print("{}: No trades of today".format(self.get_userId()))
            return

        stopl̇oss_orders = orders[orders.status == "TRIGGER PENDING"]
        if tag != "ALL":
            stopl̇oss_orders = stopl̇oss_orders[stopl̇oss_orders.tag == tag]

        if len(stopl̇oss_orders) == 0:
            print("{}: All stoploss orders have been already executed".format(self.get_userId()))
            return

        orders_to_close = list(stopl̇oss_orders.orderid.unique())

        stopl̇oss_orders = stopl̇oss_orders.to_dict('records')
        for stoploss_order in stopl̇oss_orders:
            exchange = stoploss_order['exchange']
            tradingsymbol = stoploss_order['tradingsymbol']

            if exchange == "NFO":
                stoploss_order['order_type'] = "MARKET"
                stoploss_order['price'] = 0
            else:
                ltp = self.get_ltp(exchange, tradingsymbol)
                stoploss_order['order_type'] = "LIMIT"
                stoploss_order['price'] = ltp

            self.modify_order(stoploss_order)
            time.sleep(.1)

        self.modify_orders_till_complete(orders_to_close)
        self.positions_pnl()

    def add_params(self, orders):
        df = pd.DataFrame(orders)
        df.loc[:, 'price'] = df.apply(lambda x: self.get_ltp(x['exchange'],
                                                             x['tradingsymbol']),
                                      axis=1)

        df.loc[:, 'disclosedquantity'] = np.where(df.exchange == "NSE", df.quantity/10 + 1, df.quantity)
        df.loc[:, 'disclosedquantity'] = df.disclosedquantity.astype(int)

        return df.to_dict('records')


    # @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def place_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                    tag=None, product=None, price=None, trigger_price=None):
        try:
            order_id = self.wrapper.place_order(variety='regular',
                                                tradingsymbol=tradingsymbol,
                                                exchange=exchange,
                                                transaction_type=transaction_type,
                                                quantity=int(abs(quantity)),
                                                order_type=order_type,
                                                disclosed_quantity=None,
                                                price=price,
                                                trigger_price=trigger_price,
                                                product=product,
                                                tag=tag)
            return order_id
        except Exception as e:
            exception_message = "Order placement failed with error [{}]".format(str(e))
            print(exception_message)

    def configure(self):
        quantplay_config = QplayConfig.get_config()

        print("Enter Zerodha API key:")
        api_key = input()

        print("Enter Zerodha API Secret:")
        api_secret = input()

        quantplay_config['DEFAULT'][Zerodha.zerodha_api_key] = api_key
        quantplay_config['DEFAULT'][Zerodha.zerodha_api_secret] = api_secret

        with open('{}/config'.format(QplayConfig.config_path), 'w') as configfile:
            quantplay_config.write(configfile)

    def validate_config(self, quantplay_config):
        if quantplay_config is None:
            return False
        if Zerodha.zerodha_api_key not in quantplay_config['DEFAULT']:
            return False
        if Zerodha.zerodha_api_secret not in quantplay_config["DEFAULT"]:
            return False

        return True

    def generate_token(self):
        quantplay_config = QplayConfig.get_config()

        if not self.validate_config(quantplay_config):
            self.configure()
            quantplay_config = QplayConfig.get_config()

        api_key = quantplay_config['DEFAULT']['zerodha_api_key']
        api_secret = quantplay_config['DEFAULT']['zerodha_api_secret']
        kite = KiteConnect(api_key=api_key)

        request_token = None
        try:
            request_token = KiteUtils.get_request_token(kite_api_key=api_key)
        except Exception as e:
            traceback.print_exc()
            print("Need token input " + kite.login_url())
            raise e
            # request_token = input()

        print("request token {} api_secret {}".format(request_token, api_secret))

        data = kite.generate_session(request_token, api_secret=api_secret)
        kite.set_access_token(data["access_token"])

        QplayConfig.save_config("zerodha_wrapper", codecs.encode(pickle.dumps(kite), "base64").decode())
        return kite

    def option_symbol(self, underlying_symbol, expiry_date, strike_price, type):
        option_symbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[underlying_symbol]
        option_symbol += expiry_date.strftime('%y')

        month_number = str(int(expiry_date.strftime("%m")))
        monthly_option_prefix = expiry_date.strftime("%b").upper()

        if int(month_number) >= 10:
            week_option_prefix = monthly_option_prefix[0]
        else:
            week_option_prefix = month_number
        week_option_prefix += expiry_date.strftime("%d")

        next_expiry = expiry_date + timedelta(days=7)

        if next_expiry.month != expiry_date.month:
            option_symbol += monthly_option_prefix
        else:
            option_symbol += week_option_prefix

        option_symbol += str(int(strike_price))
        option_symbol += type

        return option_symbol
