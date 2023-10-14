import time
import pyautogui
from save_copied_text import get_clipboard_content
import pandas as pd

# x, y = pyautogui.position()
# print(f'Mouse coordinates: x={x}, y={y}')

while True:
    d = {
        'BANKBARODA': [(860, 249), (1517, 191), (1582, 191)]
    }

    # Set the coordinates

    copy_table = d['BANKBARODA'][0]
    table = d['BANKBARODA'][1]
    refresh = d['BANKBARODA'][2]

    # Press Alt + Tab
    pyautogui.hotkey('alt', 'tab')

    time.sleep(1)
    # Perform a left click
    pyautogui.click(refresh)
    time.sleep(10)
    pyautogui.click(table)
    time.sleep(1)
    pyautogui.click(copy_table)
    time.sleep(1)

    # Press Alt + Tab
    pyautogui.hotkey('alt', 'tab')

    text_data = get_clipboard_content()

    with open('output.csv', 'w') as f:
        f.write(text_data)


    df = pd.read_csv('output.csv')
    df = df[::-1]

    ma_50 = df["MA ‌ma‌ (50,ma,0)"].to_list()
    ma_20 = df["MA ‌ma‌ (20,ma,0)"].to_list()

    if (ma_20[1] < ma_50[1]) and (ma_20[0] == ma_50[0]):
        print("BUYyyyyyyyy")

    if (ma_20[1] > ma_50[1]) and (ma_20[0] == ma_50[0]):
        print("SELLlllllll")

    time.sleep(180)