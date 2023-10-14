import requests
import json
import time

from kiteconnect import KiteConnect, KiteTicker
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


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
api_key = '30wyfm3oykkug4de'
api_secret = 'efd25m5zsjvaql766r3xqiwl50r0bsvn'


kite = KiteConnect(api_key=api_key)

request_token = 'gj49eXrAXJtl9jc7ujT74zLGfBk84CYz'


kite.set_access_token("HrqxIwMIq1PqBNF38ERKteZ3arSENosz")

positions = kite.positions()["day"]

for position in positions:
    print(position["tradingsymbol"], position, "\n")




# times = []

# for i in range(9, 16):
#     for j in range(0, 60, 2):
#         times.append([i,j])

# # print(times[9:-29])  #last time set at 15:00 hrs

# scheduler = BlockingScheduler()

# for i in range(len(times[9:-29])):
#     scheduler.add_job(core, 'cron', hour=times[i][0], minute=times[i][1], second=5)  # Set the time for execution


# scheduler.start()

# # def closePos():

