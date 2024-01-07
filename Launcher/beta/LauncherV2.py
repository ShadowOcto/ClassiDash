import os

import requests
from utils import *
import threading
import zipfile

timer = 0
stage = 0
downloadDir = 'C:\\cdDevelopment'
title = 'ClassiDash Launcher v2.0.0'
if os.name == 'nt': os.system(f"title {title}")

def download():
    console.log("Started GDPS Download", '')
    r = requests.get('https://classidash.fun/download', allow_redirects=True)
    open(f'{downloadDir}/client.zip', 'wb').write(r.content)
    console.log(f"Completed GDPS Download ({timer}s)", 's')


console.clear()
console.cPrint(title)

if not os.path.isdir(downloadDir): os.mkdir(downloadDir)

if not os.path.isfile(f'{downloadDir}/version'): open(f'{downloadDir}/version', 'w+')
try:
    verRequest = requests.get('https://classidash.fun/api/version').text
except:
    console.log("Failed to connect to server", 'f')
    console.log("Attempting to launch GDPS offline...", '')
    os.chdir(f'{downloadDir}\\ClassiDash\\'); os.system(f'.\\ClassiDash.exe')
    quit(0)

ver = open(f'{downloadDir}/version', 'r').read()

if not ver == verRequest: stage = 1

# Update GDPS
if stage == 1:
    threading.Thread(target=download).start()
    while threading.activeCount() == 2:
        console.spinner(1, 'Downloading... (' + str(timer) + "s)")
        timer = timer + 1

    console.log("Started GDPS Extraction", '')
    with zipfile.ZipFile(f'{downloadDir}/client.zip', 'r') as zip_ref:
        zip_ref.extractall(downloadDir)
    console.log(f"Completed GDPS Extraction", 's')

    os.remove(f'{downloadDir}/client.zip')
    console.log("Deleted client.zip", '')
    open(f'{downloadDir}/version', 'w').write(verRequest)
    console.log("Updated local version", '')
    console.log("Update Completed", 's')

console.log("Launching GDPS...", 's')
os.chdir(f'{downloadDir}\\ClassiDash\\'); os.system(f'.\\ClassiDash.exe')
