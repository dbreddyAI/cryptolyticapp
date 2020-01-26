import pandas as pd
import psycopg2 as ps
from config import POSTGRES_DBNAME, POSTGRES_PASSWORD, POSTGRES_USERNAME, POSTGRES_PORT, POSTGRES_ADDRESS, API_KEY



# dictionary used to rename column values with correct time period
model_periods = {'bitfinex_ltc_usd': '1440T',
                 'bitfinex_btc_usd':'1200T',
                 'bitfinex_eth_usd': '1200T',
                 'hitbtc_ltc_usdt': '1440T',
                 'hitbtc_btc_usdt': '360T',
                 'hitbtc_eth_usdt': '1440T',
                 'coinbase_pro_btc_usd': '960T',
                 'coinbase_pro_eth_usd': '960T',
                 'coinbase_pro_ltc_usd': '960T'}

# Insert DB Credentials - Don't push to GH
credentials = {'POSTGRES_ADDRESS': POSTGRES_ADDRESS,
               'POSTGRES_PORT': POSTGRES_PORT,
               'POSTGRES_USERNAME': POSTGRES_USERNAME,
               'POSTGRES_PASSWORD': POSTGRES_PASSWORD,
               'POSTGRES_DBNAME': POSTGRES_DBNAME,
               'API_KEY': API_KEY
               }

def create_conn(credentials):
    """ Function that creates a connection with DB """

    # creating connection
    conn = ps.connect(host=credentials['POSTGRES_ADDRESS'],
                      database=credentials['POSTGRES_DBNAME'],
                      user=credentials['POSTGRES_USERNAME'],
                      password=credentials['POSTGRES_PASSWORD'],
                      port=credentials['POSTGRES_PORT'])

    # creating cursor
    cur = conn.cursor()

    return conn, cur

def display_tr_pred():
    """
    Retrieves trade recommender predictions from DB and returns result in JSON format
    """

    # create connection and cursor
    conn, cur = create_conn(credentials)

    # Gets last 20 prediction results from trp table
    cur.execute("""SELECT * FROM tr_pred
                    ORDER by time desc limit 10;""")

    result = cur.fetchall()

    # creates dataframe from results and rename columns
    result = pd.DataFrame(result)
    result = result.rename(columns={0: 'time', 1: 'exchange', 2: 'trading_pair', 3: 'prediction'})

    # filter predictions to get one for each combination
    result = result.drop_duplicates(subset=['exchange','trading_pair'])

    # creating new column with exchange_trading_pair name combined
    result['period'] = result['exchange'] +'_'+ result['trading_pair']
    # use the values in period to rename them with the dict 'model_periods' values
    result['period'] = result['period'].apply(lambda x: model_periods[x])

    # close connection
    conn.close()

    return result

def display_arb_pred():
    """
    Retrieves arbitrage predictions from DB and returns result in JSON format
    """

    # create connection and cursor
    conn, cur = create_conn(credentials)

    # Gets last 500 prediction results from arp table
    cur.execute("""SELECT * FROM arb_pred
                   ORDER by time desc limit 10;""")
    result = cur.fetchall()

    # creates dataframe from results and rename columns
    result = pd.DataFrame(result)
    result = result.rename(
        columns={0: 'time', 1: 'exchange_1', 2: 'exchange_2', 3: 'trading_pair', 4: 'prediction'})

    # result = result.drop(columns='c_time')
    result = result.drop_duplicates(subset=['exchange_1', 'exchange_2', 'trading_pair'])

    # close connection to DB
    conn.close()
    return result