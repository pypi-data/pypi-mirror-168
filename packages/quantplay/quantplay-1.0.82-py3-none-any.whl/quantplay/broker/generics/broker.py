from quantplay.utils.constant import Constants
from collections import defaultdict
from quantplay.utils.exchange import Market as MarketConstants
from datetime import timedelta

class Broker():

    def __init__(self):
        self.instrument_id_to_symbol_map = dict()
        self.instrument_id_to_exchange_map = dict()
        self.instrument_id_to_security_type_map = dict()
        self.exchange_symbol_to_instrument_id_map = defaultdict(dict)

    def round_to_tick(self, number):
        return round(number * 20) / 20

    def populate_instruments(self, instruments):
        """Fetches instruments for all exchanges from the broker
        and stores them in the member attributes.
        """
        Constants.logger.info("populating instruments")
        for instrument in instruments:
            exchange, symbol, instrument_id = (
                instrument.exchange,
                instrument.symbol,
                instrument.instrument_id,
            )
            self.instrument_id_to_symbol_map[instrument_id] = symbol
            self.instrument_id_to_exchange_map[instrument_id] = exchange
            self.instrument_id_to_security_type_map[
                instrument_id
            ] = instrument.security_type()
            self.exchange_symbol_to_instrument_id_map[exchange][symbol] = instrument_id

    def execute_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                      stoploss=None, tag=None, product=None, price=None):
        if price is None:
            price = self.get_ltp(exchange=exchange, tradingsymbol=tradingsymbol)
        try:
            if stoploss != None:
                if transaction_type == "SELL":
                    sl_transaction_type = "BUY"
                    sl_trigger_price = self.round_to_tick(price*(1+stoploss))

                    if exchange == "NFO":
                        price = sl_trigger_price*1.05
                    elif exchange == "NSE":
                        price = sl_trigger_price * 1.01
                    else:
                        raise Exception("{} not supported for trading".format(exchange))

                    sl_price = self.round_to_tick(price)
                elif transaction_type == "BUY":
                    sl_transaction_type = "SELL"
                    sl_trigger_price = self.round_to_tick(price * (1 - stoploss))

                    if exchange == "NFO":
                        price = sl_trigger_price*.95
                    elif exchange == "NSE":
                        price = sl_trigger_price * .99
                    else:
                        raise Exception("{} not supported for trading".format(exchange))

                    sl_price = self.round_to_tick(price)
                else:
                    raise Exception("Invalid transaction_type {}".format(transaction_type))
                self.place_order(tradingsymbol=tradingsymbol, exchange=exchange, quantity=quantity,order_type="SL",
                                 transaction_type=sl_transaction_type, tag=tag,product=product, price=sl_price,
                                 trigger_price=sl_trigger_price)

            if order_type == "MARKET":
                price = 0

            response = self.place_order(tradingsymbol=tradingsymbol, exchange=exchange, quantity=quantity,
                                        order_type=order_type, transaction_type=transaction_type, tag=tag,
                                        product=product, price=price)
            return response
        except Exception as e:
            raise e

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
