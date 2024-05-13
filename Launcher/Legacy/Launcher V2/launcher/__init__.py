import os
import time

import requests
from utils import *
import threading
import zipfile

downloadDir = 'C:\\cdDevelopment'

def launch(skip):
    timer = 0
    stage = 0
    title = 'ClassiDash Launcher v2.0.0'
    if os.name == 'nt': os.system(f"title {title}")

    console.clear()

    def download():
        console.log("Started GDPS Download", '')
        r = requests.get('https://classidash.fun/download', allow_redirects=True)
        open(f'{downloadDir}/client.zip', 'wb').write(r.content)
        console.log(f"Completed GDPS Download ({timer}s)", 's')

    os.system('cls' if os.name == 'nt' else 'clear')
    console.cPrint(title)

    if not os.path.isdir(downloadDir): os.mkdir(downloadDir)

    if not os.path.isfile(f'{downloadDir}/version'): open(f'{downloadDir}/version', 'w+')
    ver = open(f'{downloadDir}/version', 'r').read()

    try:
        verRequest = requests.get('https://classidash.fun/api/version').text
    except:
        verRequest = ver
        console.log("Failed to connect to server (1A)", 'f')
        console.log("Attempting to launch GDPS offline...", '')
        os.chdir(f'{downloadDir}\\ClassiDash\\');
        os.system(f'start .\\ClassiDash.exe')

    def get_size(path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def extract():
        with zipfile.ZipFile(f'{downloadDir}/client.zip', 'r') as zip_ref:
            zip_ref.extractall(downloadDir)

    if skip == 0 or skip == 2: stage = 1
    if ver == verRequest and skip == 0: stage = 0

    # Update GDPS
    if stage == 1:
        if skip == 0: inp = input("There is an update available, would you like to download it? [Y/N] : ")

        if inp.lower() == 'y':
            threading.Thread(target=download).start()
            while threading.activeCount() == 2:
                if timer < 30: console.spinner(1, 'Downloading... (' + str(timer) + "s)")
                else: console.spinner(1, 'Downloading... (' + str(timer) + "s) (You may have to restart your launcher.)")
                timer = timer + 1

            console.log("Started GDPS Extraction", '')
            threading.Thread(target=extract).start()
            while threading.activeCount() == 2:
                console.progressBar((int(get_size(f'{downloadDir}/ClassiDash/') / 1048576) / 10), 20, 'Extracting...')
            console.progressBar(20, 20, 'Extracting...')
            console.log(f"Completed GDPS Extraction", 's')

            os.remove(f'{downloadDir}/client.zip')
            console.log("Deleted client.zip", '')
            open(f'{downloadDir}/version', 'w').write(verRequest)
            console.log("Updated local version", '')
            console.log("Update Completed", 's')

    console.log("Launching GDPS...", 's')
    try:
        os.chdir(f'{downloadDir}\\ClassiDash\\')
        os.system(f'start .\\ClassiDash.exe')
        console.log("Launched GDPS!", 's')
        time.sleep(5)
    except:
        if skip == 0:
            console.log("Failed to launch GDPS, Redownloading... (1B)", 'f')
            time.sleep(2)
            launch(2)
        else:
            console.log("Failed to launch GDPS. (1C)", 'f')
            time.sleep(2)

