import pandas as pd
import psycopg2 as ps
import datetime as dt
from datetime import datetime
from dateutil import tz
from config import POSTGRES_DBNAME, POSTGRES_PASSWORD, POSTGRES_USERNAME, POSTGRES_PORT, POSTGRES_ADDRESS, API_KEY

""" Functions for Flask App """

# dict with available exchange/trading pair for trade predictions
exchanges={'bitfinex': ['btc_usd', 'eth_usd', 'ltc_usd'],
           'coinbase_pro': ['btc_usd', 'eth_usd', 'ltc_usd'],
           'hitbtc': ['btc_usdt', 'eth_usdt', 'ltc_usdt']}

# Insert DB Credentials - Don't push to GH
credentials = {'POSTGRES_ADDRESS': POSTGRES_ADDRESS,
               'POSTGRES_PORT': POSTGRES_PORT,
               'POSTGRES_USERNAME': POSTGRES_USERNAME,
               'POSTGRES_PASSWORD': POSTGRES_PASSWORD,
               'POSTGRES_DBNAME': POSTGRES_DBNAME,
               'API_KEY': API_KEY
               }


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


def retrieve_one_trp(exchange, trading_pair, model_periods):
    """ Retrieve the last trade recommender prediction from DB """

    # to retrieve period of trp model
    period = model_periods[exchange + '_' + trading_pair]

    # create connection and cursor
    conn, cur = create_conn(credentials)

    # Change limit number to whatever amount of rows you want to retrieve
    cur.execute("""SELECT * FROM tr_pred
                    WHERE exchange = '{exchange}'
                    AND trading_pair = '{trading_pair}'
                    ORDER by p_time desc limit 1;""".format(trading_pair=trading_pair, exchange=exchange))

    result = cur.fetchall()

    # creates dataframe from results and rename columns
    result = pd.DataFrame(result)
    result = result.rename(
        columns={0: 'p_time', 1: 'c_time', 2: 'exchange', 3: 'trading_pair', 4: 'prediction'})

    # get the one value in p_time
    pt = result['p_time'].values

    # get UTC timezone
    from_zone = tz.gettz('UTC')
    # get PST timezone
    to_zone = tz.gettz('US/Pacific')
    utc = datetime.strptime(str(pt[0]), '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    pcf = utc.astimezone(to_zone)

    # returning new timezone value to the df
    result['p_time'] = str(pcf)[:-6]

    # creating df to dictionary
    result = result.to_dict()

    # add the new period key and value to dictionary
    result.update({'period': period})

    # close connection
    conn.close()

    return result


# This is for retrieving arbitrage predictions from DB
def retrieve_one_arb(exchange_1, exchange_2, trading_pair):
    ''' Retrieve the last arbitrage prediction from DB '''

    # create connection and cursor
    conn, cur = create_conn(credentials)

    try:
        cur.execute("""SELECT * FROM prediction.arp
                    WHERE exchange_1 = '{exchange_2}'
                    AND exchange_2 = '{exchange_1}'
                    AND trading_pair = '{trading_pair}'
                    OR exchange_1 = '{exchange_1}'
                    AND exchange_2 = '{exchange_2}'
                    AND trading_pair = '{trading_pair}'
                    ORDER by p_time desc limit 1;""".format(trading_pair=trading_pair, exchange_2=exchange_2, exchange_1=exchange_1))

        result = cur.fetchall()

        # creates dataframe from results and rename columns
        result = pd.DataFrame(result)
        result = result.rename(
            columns={0: 'p_time', 1: 'c_time', 2: 'exchange_1', 3: 'exchange_2', 4: 'trading_pair', 5: 'prediction'})

        # get the one value in p_time
        pt = result['p_time'].values

        # get UTC time zone
        from_zone = tz.gettz('UTC')
        # get PST time zone
        to_zone = tz.gettz('US/Pacific')
        utc = datetime.strptime(str(pt[0]), '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        pcf = utc.astimezone(to_zone)

        # returning new timezone value to the df
        result['p_time'] = str(pcf)[:-6]

        # creating df to dictionary
        result = result.to_dict()

        # closing connection
        conn.close()

        return result

    except:
        pass


def retrieve_tr_pred():
    """ 
    Retrieves trade recommender predictions from DB and returns result in JSON format
    """

    # create connection and cursor
    conn, cur = create_conn(credentials)

    # Gets last 20 prediction results from trp table
    cur.execute("""SELECT * FROM tr_pred
                    ORDER by p_time desc limit 500;""")

    result = cur.fetchall()

    # creates dataframe from results and rename columns
    result = pd.DataFrame(result)
    result = result.rename(columns={0: 'p_time', 1: 'c_time', 2: 'exchange', 3: 'trading_pair', 4: 'prediction'})

    # filter predictions to get one for each combination
    result = result.drop_duplicates(subset=['exchange','trading_pair'])

    # creating new column with exchange_trading_pair name combined
    result['period'] = result['exchange'] +'_'+ result['trading_pair']
    # use the values in period to rename them with the dict 'model_periods' values
    result['period'] = result['period'].apply(lambda x: model_periods[x])

    # drop unnecessary columns
    result.drop(columns=['c_time'], inplace=True)

    # Creating List of prediction time values
    pt = result['p_time'].values

    # getting UTC timezone
    from_zone = tz.gettz('UTC')
    # getting PST timezone
    to_zone = tz.gettz('US/Pacific')

    nt = []
    # Looping thru 'p_time' values to change time to PST
    for p in pt:
        utc = datetime.strptime(str(p), '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        pcf = utc.astimezone(to_zone)

        # append new PST time to nt list
        nt.append(str(pcf)[:-6] + ' PST')

    # Give new PST time value to 'p_time" column
    result['p_time'] = nt

    # Create json output 
    result = (result.groupby(['exchange', 'trading_pair'], as_index=True)
                    .apply(lambda x: x[['p_time', 'period', 'prediction']].to_dict('r')).to_dict())

    # close connection
    conn.close()

    return result


def retrieve_arb_pred():
    """
    Retrieves arbitrage predictions from DB and returns result in JSON format
    """

    # create connection and cursor
    conn, cur = create_conn(credentials)

    # Gets last 500 prediction results from arp table
    cur.execute("""SELECT * FROM prediction.arp
                   ORDER by p_time desc limit 500;""")
    result = cur.fetchall()

    # creates dataframe from results and rename columns
    result = pd.DataFrame(result)
    result = result.rename(
        columns={0: 'p_time', 1: 'c_time', 2: 'exchange_1', 3: 'exchange_2', 4: 'trading_pair', 5: 'prediction'})

    # result = result.drop(columns='c_time')
    result = result.drop_duplicates(subset=['exchange_1', 'exchange_2', 'trading_pair'])

    # converts p_time column to datetime 
    result['datetime'] = pd.to_datetime(result['p_time'])

    # create time threshold to 15 minutes, to only return results in the last 15 min
    # filters result to the last 15 min
    t = dt.datetime.now() - dt.timedelta(minutes=15)
    result = result[result['datetime'] > t]

    # drop unnecessary columns
    result.drop(columns=['datetime', 'c_time'], inplace=True)

    # creating a list of prediction time values
    pt = result['p_time'].values

    # Getting UTC timezone
    from_zone = tz.gettz('UTC')
    # Getting PST timezone
    to_zone = tz.gettz('US/Pacific')

    nt = []
    # Looping thru 'p_time' values to change time to PST
    for p in pt:
        utc = datetime.strptime(str(p), '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        pcf = utc.astimezone(to_zone)

        # appends new time to nt list
        nt.append(str(pcf)[:-6] + ' PST')

    # give new PST time value to 'p_time" column
    result['p_time'] = nt

    # Create json output 
    result = (result.groupby(['exchange_1', 'exchange_2', 'trading_pair'], as_index=True)
                    .apply(lambda x: x[['p_time', 'prediction']].to_dict('r')).to_dict())

    # close connection to DB
    conn.close()
    return result

