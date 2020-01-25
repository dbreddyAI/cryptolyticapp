from flask import Flask, jsonify, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils import create_conn, retrieve_one_trp, credentials, retrieve_one_arb, retrieve_arb_pred, retrieve_tr_pred


application = Flask(__name__)


@application.route('/')
def index():
    """Homepage"""
    return render_template('index.html') 

limiter = Limiter(
    application,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# testing rate limit
@application.route('/ratelimittest')
@limiter.limit("60 per minute")
def slow():
    return "rate limit"


@application.route('/crypto', methods=['POST'])
def crypto_trade_predictions():
    """ Takes in data from crypto exchanges and returns an output for whether
        the model predicts the price of a coin will go up or down in the next
        1 hour period.

        Supported Exchange/Trading Pairs:
            - bitfinex
                - 'btc_usd'
                - 'eth_usd'
                - 'ltc_usd'
            - coinbase_pro
                - 'btc_usd'
                - 'eth_usd'
                - 'ltc_usd'
            - hitbtc
                - 'btc_usdt'
                - 'eth_usdt'
                - 'ltc_usdt'

        Sample request:
        post = { "exchange" : "bitfinex",
                 "trading_pair" : "btc_usd" }
        """

    # dictionary for model periods
    model_periods = {'bitfinex_ltc_usd': '24 Hours',
                     'bitfinex_btc_usd': '20 Hours',
                     'bitfinex_eth_usd': '20 Hours',
                     'hitbtc_ltc_usdt': '24 Hours',
                     'hitbtc_btc_usdt': '6 Hours',
                     'hitbtc_eth_usdt': '24 Hours',
                     'coinbase_pro_btc_usd': '16 Hours',
                     'coinbase_pro_eth_usd': '16 Hours',
                     'coinbase_pro_ltc_usd': '16 Hours'}

    # request data
    exchange = request.form.get('exchange')
    trading_pair = request.form.get('trading_pair')

    # HitBTC needs a t at the end for usd pairings
    if exchange == 'hitbtc':
        trading_pair = trading_pair + 't'

    predictions = retrieve_one_trp(exchange, trading_pair, model_periods)

    return render_template("result.html", results=predictions)


# Route for arbitrage prediction
@application.route('/arb', methods=['POST'])
def arbritage_predictions():
    """ Function getting user input and returning arbitrage prediction """

    # request data
    exchange_1 = request.form.get('exchange_1')
    exchange_2 = request.form.get('exchange_2')
    trading_pair = request.form.get('trading_pair')

    # Hitbtc don't have usd pairs
    if exchange_1 == 'hitbtc':
        if trading_pair.split('_')[1] == 'usd':
            trading_pair = trading_pair + 't'
    if exchange_2 == 'hitbtc':
        if trading_pair.split('_')[1] == 'usd':
            trading_pair = trading_pair + 't'

    predictions = retrieve_one_arb(exchange_1, exchange_2, trading_pair)
    try:
        return render_template("resultarb.html", results=predictions)
    except:
        return render_template('error.html')


@application.route('/trade', methods=['GET'])
@limiter.limit("10 per minute")
def tr_predictions():
    """ Retrieve all trade predictions available """

    predictions = retrieve_tr_pred()
    return jsonify(results=str(predictions))


@application.route('/arbitrage', methods=['GET'])
@limiter.limit("60 per minute")
def arbritage_predictions1():
    """ Retrieve all arbitrage predictions available"""

    predictions = retrieve_arb_pred()
    return jsonify(results=str(predictions))


if __name__ == '__main__':
    application.run(port=5000, debug=True)
