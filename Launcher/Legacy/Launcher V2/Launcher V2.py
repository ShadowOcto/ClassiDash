import curses
import os
import time
import webbrowser
import requests

import launcher
from utils import *

console.clear()
title = 'ClassiDash Launcher v2.0.0'
if os.name == 'nt': os.system(f"title {title}")

print("Loading Launcher...")

menu = ['🚀 Launch', '🚀 Launch Offline', '💻 Dashboard', '📁 Open AppData', '📁 Open GDPS Folder', '📱 Discord', '🚪 Exit']

try: news = requests.get("https://classidash.fun/api/news").text.splitlines()
except: news = ['Failed to connect to server.', ' ']

def openFolder(path):
    os.system(f'start {path}')
    console.log(f'Attempted to open "{path}"', '')

def buttonAction(button_idx):
    curses.endwin()
    if button_idx == 0: launcher.launch(0)
    if button_idx == 1: launcher.launch(1)
    if button_idx == 2: console.log("Opened Dashboard", 's'); webbrowser.open('https://classidash.fun')
    if button_idx == 3: openFolder(f'%localappdata%\\ClassiDash\\')
    if button_idx == 4: openFolder(f'{launcher.downloadDir}')
    if button_idx == 5: console.log("Opened Discord", 's'); webbrowser.open('https://classidash.fun/discord')
    if button_idx == 6: quit(0)

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    cText = "Launcher developed by ShadowOcto"

    x = w // 2
    y = h // 2

    stdscr.addstr(0, 0, title)
    stdscr.addstr(1, 0, "Use your arrow keys ⬆ ⬇")
    stdscr.addstr((y * 2) - 1, 0, cText)
    # stdscr.addstr(0, (x - len(news) // 2) * 2, news)
    stdscr.addstr((y * 2) - 1, (x * 2) - len("▣ ClassiDash "), "▣ ClassiDash")

    for idx, row in enumerate(news):
        nx = (x * 2) - len(row)
        ny = idx
        stdscr.addstr(ny, nx, row)

    for idx, row in enumerate(menu):
        x = 1
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx: stdscr.attron(curses.color_pair(1))
        stdscr.addstr(y, x, row)
        if idx == selected_row_idx: stdscr.attroff(curses.color_pair(1))

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0

    print_menu(stdscr, current_row_idx)

    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_F3:
            curses.endwin()
            console.progressBar(1, 3, "Displaying Logs... (Press CTRL + C to force quit.)")
            time.sleep(1)
            console.progressBar(2, 3, "Displaying Logs... (Press CTRL + C to force quit.)")
            time.sleep(1)
            console.progressBar(3, 3, "Displaying Logs... (Press CTRL + C to force quit.)")
            time.sleep(1)

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            buttonAction(current_row_idx)

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()

curses.wrapper(main)
