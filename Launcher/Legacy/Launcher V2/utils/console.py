import os
import time
from datetime import datetime
from colorama import Fore, Back

timeStamp = datetime.now()
timeStamp = timeStamp.strftime("%H:%M:%S")
history = ['']

def clear():
    history.clear()
    os.system('cls' if os.name == 'nt' else 'clear')

def log(string, status=''):
    if status.lower() == "s": status = Back.GREEN
    elif status.lower() == "f": status = Back.LIGHTRED_EX
    else: status = Back.LIGHTBLACK_EX

    formattedString = f"{status} {Back.RESET} [{timeStamp}] {string}"
    history.append(formattedString)
    print(formattedString)

def cPrint(string):
    history.append(string)
    print(string)

def progressBar(value, max, status):
    os.system('cls' if os.name == 'nt' else 'clear')
    bar = ['']
    for x in history: print(x)
    i = 0
    for x in range(max):
        if i < value: bar.append(f"{Fore.LIGHTGREEN_EX}─")
        else: bar.append(f"{Fore.LIGHTBLACK_EX}-")
        i = i + 1
    print(f"{Fore.RESET}[{''.join(bar)}{Fore.RESET}] [{value}/{max}] {Fore.LIGHTBLACK_EX}{status}{Fore.RESET}")

def printSpinner(string):
    for x in history: print(x)
    print(string)
    time.sleep(0.2)
    os.system('cls' if os.name == 'nt' else 'clear')

def spinner(cycles, status):
    os.system('cls' if os.name == 'nt' else 'clear')
    for c in range(cycles):
        printSpinner(f"∙∙∙ {status}")
        printSpinner(f"●∙∙ {status}")
        printSpinner(f"∙●∙ {status}")
        printSpinner(f"∙∙● {status}")
        printSpinner(f"∙∙∙ {status}")
    for x in history: print(x)


