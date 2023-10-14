import time
from datetime import datetime
import pyautogui
import subprocess
import pandas as pd
import io
import json
from apscheduler.schedulers.blocking import BlockingScheduler

# x, y = pyautogui.position()
# print(f'Mouse coordinates: x={x}, y={y}')

# Press Alt + Tab
pyautogui.hotkey('alt', 'tab')
time.sleep(1)

def get_clipboard_content():
    try:
        clipboard_text = subprocess.check_output(
            ['xclip', '-selection', 'clipboard', '-o'],
            universal_newlines=True
        )
        return clipboard_text.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def get_data(stamp):
    print("stamp: ", stamp)
    # print("current time: ", datetime.now())
    # Set the coordinates
    d1 = ['BEL', 'HDFCBANK', 'CANBK', 'ACC', 'EICHERMOT', 'BANKBARODA', 'DABUR', 'MUTHOOTFIN', 'ZOMATO', 'IBULHSGFIN']
    d = {
        'BEL': [(800, 258), (1587, 200), (1650, 200), 98049],
        'HDFCBANK': [(897, 258), (1587, 200), (1650, 200), 341249],
        'CANBK': [(846, 258), (1587, 200), (1650, 200), 2763265],
        'ACC': [(809, 258), (1587, 200), (1650, 200), 5633],
        'EICHERMOT': [(904, 258), (1587, 200), (1650, 200), 232961],
        'BANKBARODA': [(60 + 870, 258), (1587, 200), (1650, 200), 1195009],
        'DABUR': [(60 + 780, 258), (1587, 200), (1650, 200), 197633],
        'MUTHOOTFIN': [(60 + 868, 258), (1587, 200), (1650, 200), 6054401],
        'ZOMATO': [(60 + 807, 258), (1587, 200), (1650, 200), 6054401],
        'IBULHSGFIN': [(60 + 844, 258), (1587, 200), (1650, 200), 6054401],
        # 'IRCTC': [(60 + 766, 258), (1587, 200), (1650, 200), 6054401],
        # 'ITC': [(60 + 740, 258), (1587, 200), (1650, 200), 6054401],
    }
    # 318, 
    l = 1825-50

    all_data = {}
    for index, k in enumerate(d1):
        copy_table = d[k][0]
        table = d[k][1]
        refresh = d[k][2]
        # tab = d[k][3]
        instID = d[k][3]
        tab = [50 + (l//len(d1))*index + l//(2*len(d1)), 50]

        pyautogui.click(tab)
        time.sleep(0.8)
        pyautogui.click(refresh)	
        time.sleep(1.5)
        pyautogui.click(table)
        time.sleep(1)
        pyautogui.click(copy_table)
        time.sleep(0.3)

        flag = True

        while flag:
            try:
                text_data = get_clipboard_content()
                df = pd.read_csv(io.StringIO(text_data))
                df = df[::-1]

                ma_50 = df["MA ‌ma‌ (50,ema,0)"].to_list()
                ma_28 = df["MA ‌ma‌ (28,C,ema,0)"].to_list()
                jsonData = df.iloc[0].to_dict()
                
                # Clear the clipboard after copying the content
                subprocess.run(['xclip', '-selection', 'clipboard', '-i', '/dev/null'])
                flag = False
            except:
                time.sleep(0.3)
        
        jsonData['name'] = k
        jsonData['instID'] = instID
        jsonData['ma50'] = ma_50[:5]
        jsonData['ma28'] = ma_28[:5]

        if (ma_28[1] <= ma_50[1]) and (ma_28[0] > ma_50[0]):
            jsonData['do'] = 'BUY'
        elif (ma_28[1] >= ma_50[1]) and (ma_28[0] < ma_50[0]):
            jsonData['do'] = 'SELL'
        else:
            jsonData['do'] = 'WAIT'
        # print(jsonData)
                
        # Write jsonData to a file
        all_data[k] = jsonData

    with open('data.json', 'w') as json_file:
        json.dump(all_data, json_file)


def hello_world():
    print("hello program...")


times = []
for i in range(9, 16):
    for j in range(1, 60, 1):
        times.append([i, j])

# times = times[7:-15]
times = times[14:-30]
# print(times)


# scheduler = BlockingScheduler()
# for i in range(len(times)):
#     scheduler.add_job(get_data, 'cron', hour=times[i][0], minute=times[i][1], second=2, args=[times[i]])  # Set the time for execution
# scheduler.start()

t1 = datetime.now()
get_data([0, 0])
print("time taken: ", datetime.now() - t1)