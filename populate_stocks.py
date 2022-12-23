import config

import alpaca_trade_api as tradeapi
import psycopg2

import psycopg2.extras


connection = psycopg2.connect(host=config.DB_HOST,database=config.DB_NAME,user=config.DB_USER,password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# TEST PRINT STOCK NAMES IN THE STOCK TABLE
cursor.execute("SELECT * FROM stock;")
stocks = cursor.fetchall()
for stock in stocks:
    print(stock['name'])

# CONNECTING TO ALPACA
api = tradeapi.REST(config.API_KEY,config.API_SECRET,base_url=config.API_URL)

assets = api.list_assets()

# print(assets)
for asset in assets:
    print(f'Inserting stock {asset.name} - {asset.symbol}')
    cursor.execute('''
    INSERT INTO stock (name, symbol, exchange, is_etf)
    values (%s, %s, %s, %s)
    ''', (asset.name, asset.symbol, asset.exchange, False))

# SAVING DATA TO THE DATABASE
connection.commit()

