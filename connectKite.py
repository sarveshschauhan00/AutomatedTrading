import requests
import json
import time

from kiteconnect import KiteConnect, KiteTicker
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


# def upwards(instID):
#     transaction_type = kite.TRANSACTION_TYPE_BUY
#     quantity = 1  # Number of shares to buy
#     order_type = kite.ORDER_TYPE_MARKET
#     exchange = kite.EXCHANGE_NSE
    
#     # Place the order using the instrument token
#     try:
#         order_id = kite.place_order(
#             tradingsymbol=None,  # Set to None when using instrument_token
#             exchange=exchange,
#             transaction_type=transaction_type,
#             quantity=quantity,
#             order_type=order_type,
#             product=kite.PRODUCT_MIS,  # MIS for Intraday orders
#             instrument_token=instID,
#         )
#         print(f"Order placed successfully. Order ID: {order_id}")
#     except Exception as e:
#         print(f"Order placement failed: {e}")

def upwards1(inst):
    order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
                                tradingsymbol=inst,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=25,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_MIS,
                                validity=kite.VALIDITY_DAY)
    print(f"BUY order placed successfully. Order ID: {order_id}")


def downwards1(inst):

    order_id = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        tradingsymbol=inst,  # Replace with the symbol you want to sell
        exchange=kite.EXCHANGE_NSE,  # Replace with the appropriate exchange
        transaction_type=kite.TRANSACTION_TYPE_SELL,  # Use SELL for selling
        quantity=25,  # Number of shares to sell
        order_type=kite.ORDER_TYPE_MARKET,  # You can change the order type if needed
        product=kite.PRODUCT_MIS,  # CNC for Cash and Carry orders
        validity=kite.VALIDITY_DAY,  # DAY for intraday orders
    )
    print(f"SELL order placed successfully. Order ID: {order_id}")





def downwards(instID):
    transaction_type = kite.TRANSACTION_TYPE_SELL
    quantity = 1  # Number of shares to sell
    order_type = kite.ORDER_TYPE_MARKET
    exchange = kite.EXCHANGE_NSE

    # Place the SELL order using the instrument token
    try:
        order_id = kite.place_order(
            tradingsymbol=None,  # Set to None when using instrument_token
            exchange=exchange,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type=order_type,
            product=kite.PRODUCT_MIS,  # MIS for Intraday orders
            instrument_token=instID
        )
        print(f"SELL order placed successfully. Order ID: {order_id}")
    except Exception as e:
        print(f"SELL order placement failed: {e}")


def core():
    url = "https://c9b4-119-82-102-250.ngrok-free.app"
    print("the time is ", datetime.now() )
# to be looped from 9.15 - 2.45

    response = requests.get(url)
    json_data = response.json()

    for k in json_data:
        var50 = json_data[k]["ma50"]
        var28 = json_data[k]["ma28"]

        if ( var28[1] <= var50[1] and var28[0] > var50[0]  ):
            print(" UPUPUPUPUP ***** BUY  ***** UPUPUPUPUP ", k)
            upwards1(k)
        elif ( var28[1] >= var50[1] and var28[0] < var50[0] ):
            print(" DOWNDOWN *****   SELL ***** DOWNDOWN ", k)
            downwards1(k)
        else:
            print("No decision - on ", k)


# Your API Key and API Secret
api_key = '<api-key>'
api_secret = '<api-secret>'


kite = KiteConnect(api_key=api_key)

request_token = '<request-token>'


kite.set_access_token("<access-token>")

times = []

for i in range(9, 16):
    for j in range(0, 60, 2):
        times.append([i,j])

# print(times[9:-29])  #last time set at 15:00 hrs

scheduler = BlockingScheduler()

for i in range(len(times[9:-29])):

    scheduler.add_job(core, 'cron', hour=times[i][0], minute=times[i][1], second=5)  # Set the time for execution

# scheduler.add_job(closePos, 'cron', hour=15, minute=2, second=5)  # Set the time for execution

scheduler.start()

# def closePos():

