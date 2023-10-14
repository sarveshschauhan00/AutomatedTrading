import time
import pyautogui
from save_copied_text import get_clipboard_content
import pandas as pd
import io
import json

# x, y = pyautogui.position()
# print(f'Mouse coordinates: x={x}, y={y}')

# Set the coordinates
d = {
    'BEL': [(188, 258), (823, 198), (885, 199),(183,48), 98049],
    'HDFCBANK': [(280, 258), (823, 198), (885, 199),(321,48), 341249],
    'CANBK': [(232, 258), (823, 198), (885, 199),(463,48), 2763265],
    'ACC': [(195, 258), (823, 198), (885, 199),(599,48), 5633],
    'EICHERMOT': [(290, 258), (823, 198), (885, 199),(736,48), 232961],
}

# Press Alt + Tab
pyautogui.hotkey('alt', 'tab')
time.sleep(1)

while True:
    all_data = {}
    for k in d:

        copy_table = d[k][0]
        table = d[k][1]
        refresh = d[k][2]
        tab = d[k][3]
        instID = d[k][4]

        jsonData = {'name': k, 'instID': instID}

        pyautogui.click(tab)
        time.sleep(1)
        pyautogui.click(refresh)	
        time.sleep(3)
        pyautogui.click(table)
        time.sleep(1)
        pyautogui.click(copy_table)
        time.sleep(1)

        text_data = get_clipboard_content()

        df = pd.read_csv(io.StringIO(text_data))
        df = df[::-1]

        ma_50 = df["MA ‌ma‌ (50,ema,0)"].to_list()
        ma_28 = df["MA ‌ma‌ (28,C,ema,0)"].to_list()
        jsonData['data'] = df.iloc[0].to_dict()

        if (ma_28[1] == ma_50[1]) and (ma_28[0] < ma_50[0]):
            jsonData['do'] = 'BUY'
        elif (ma_28[1] == ma_50[1]) and (ma_28[0] > ma_50[0]):
            jsonData['do'] = 'SELL'
        else:
            jsonData['do'] = 'WAIT'
        print(jsonData)
                
        # Write jsonData to a file
        all_data[k] = jsonData

    with open('data.json', 'w') as json_file:
        json.dump(all_data, json_file)
        
    time.sleep(120 - 30)
