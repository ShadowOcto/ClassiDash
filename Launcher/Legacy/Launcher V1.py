import os
import customtkinter as ctk
import requests
from PIL import Image

# Create files directory
if not os.path.isdir('./files/'):
    os.system("mkdir .\\files\\")

# Init status variables
buildStatus = "Offline"
buttonStatus = "Launch"

# Download assets from server
try:
    # Version File
    ver = requests.get("https://classidash.fun/api/version").text
    if os.path.isfile('./files/version'):
        verRequest = requests.get("https://classidash.fun/api/version")
        offlineVersion = open('./files/version', 'r').read().strip()

    # Client Updater
    if not os.path.isfile("./files/updater.bat"):
        updater = requests.get("https://classidash.fun/updater")
        open('./files/updater.bat', 'wb').write(updater.content)
    # Favicon
    if not os.path.isfile("./files/favicon.ico"):
        updater = requests.get("https://classidash.fun/assets/favicon.ico")
        open('./files/favicon.ico', 'wb').write(updater.content)

    # Rocket Icon
    if not os.path.isfile('./files/rocket.png'):
        r = requests.get("https://classidash.fun/assets/rocket.png")
        open('./files/rocket.png', 'wb').write(r.content)
    # Folder Icon
    if not os.path.isfile('./files/folder.png'):
        r = requests.get("https://classidash.fun/assets/folder.png")
        open('./files/folder.png', 'wb').write(r.content)
    # Discord Icon
    if not os.path.isfile('./files/discord.png'):
        r = requests.get("https://classidash.fun/assets/discord.png")
        open('./files/discord.png', 'wb').write(r.content)
    # Desktop Icon
    if not os.path.isfile('./files/desktop.png'):
        r = requests.get("https://classidash.fun/assets/desktop.png")
        open('./files/desktop.png', 'wb').write(r.content)

    # Background
    r = requests.get("https://classidash.fun/assets/bg.png")
    open('./files/bg.png', 'wb').write(r.content)
except:
    buildStatus = "Offline"

# Init Window
window = ctk.CTk()
window.title("ClassiDash Launcher")
window.resizable(False, False)
window.geometry('820x480')
if os.path.isfile("./files/favicon.ico"): window.iconbitmap("./files/favicon.ico")

# Check if version is outdated
if os.path.isfile('./files/version'):
    try:
        if int(offlineVersion) != int(ver):
            buildStatus = "Outdated!"
        elif int(offlineVersion) == int(ver):
            buildStatus = "Current"
    except:
        buildStatus = "Offline"
else:
    buildStatus = "Not Downloaded"

if (buildStatus == "Not Downloaded"): buttonStatus = "Download"

def joinDiscordServer(): os.system("start https://classidash.fun/discord")
def openDashboard(): os.system("start https://classidash.fun/dashboard")
def openResources(): os.system("start .\\files\\ClassiDash\\Resources\\")
def openAppdata(): os.system("start %localappdata%\\ClassiDash\\")

def launchClientOffline(): os.system("cd .\\files\\ClassiDash\\ && start ClassiDash.exe")

def launchClient():
    if not os.path.isfile("./files/version"):
        os.system(f"echo {ver} > .\\files\\version")
        os.system("start .\\files\\updater.bat")
    else:
        try:
            if int(offlineVersion) != int(ver):
                os.system(f"echo {ver} > .\\files\\version")
                os.system("start .\\files\\updater.bat")
                r = requests.get("https://classidash.fun/assets/bg.png")
                open('./files/bg.png', 'wb').write(r.content)
            else:
                launchClientOffline()
        except:
            launchClientOffline()
    window.quit()
    quit()

# GUI
rocket_icon = ctk.CTkImage(Image.open("./files/rocket.png"), size=(20, 20))
folder_icon = ctk.CTkImage(Image.open("./files/folder.png"), size=(20, 20))
discord_icon = ctk.CTkImage(Image.open("./files/discord.png"), size=(20, 20))
desktop_icon = ctk.CTkImage(Image.open("./files/desktop.png"), size=(20, 20))

bg = ctk.CTkImage(Image.open("./files/bg.png"), size=(820, 415))
back = ctk.CTkLabel(master=window, text="", image=bg)
back.place(x=0, y=0)

bar = ctk.CTkFrame(master=window, corner_radius=0, fg_color="transparent")
bar.place(x=0, y=412, relheight=1.0, relwidth=1.0)

label_1 = ctk.CTkLabel(text=f"ClassiDash ({buildStatus})", master=bar, justify=ctk.LEFT, font=ctk.CTkFont(size=15), fg_color="transparent")
label_1.place(x=20, y=20)

text_1 = ctk.CTkTextbox(master=window, width=300, height=100, corner_radius=0)
try:
    text_1.insert("0.0", requests.get("https://classidash.fun/api/news").text)
except:
    text_1.insert("0.0", "Failed to connect to the server.")
text_1.configure(state=ctk.DISABLED)
text_1.place(x=510, y=5)

discord_button = ctk.CTkButton(master=window, text="Join Discord Server",image=discord_icon, font=ctk.CTkFont(size=15), command=joinDiscordServer)
dashboard_button = ctk.CTkButton(master=window, text="Open Dashboard",image=desktop_icon, font=ctk.CTkFont(size=15), command=openDashboard)
resources_button = ctk.CTkButton(master=window, text="Open Resources",image=folder_icon, font=ctk.CTkFont(size=15), command=openResources)
songs_button = ctk.CTkButton(master=window, text="Open AppData",image=folder_icon, font=ctk.CTkFont(size=15), command=openAppdata)

launch_button = ctk.CTkButton(master=bar, text=buttonStatus,image=rocket_icon, font=ctk.CTkFont(size=15), command=launchClient)
launch_button.place(x=670, y=20)
launchOffline_button = ctk.CTkButton(master=bar, text=f"Launch (Offline)", font=ctk.CTkFont(size=13), width=100, command=launchClientOffline)

if buttonStatus != "Download": launchOffline_button.place(x=555, y=20)
discord_button.place(x=5, y=5)
dashboard_button.place(x=5, y=40)
if buttonStatus != "Download": resources_button.place(x=5, y=75)
if buttonStatus != "Download": songs_button.place(x=5, y=110)

window.mainloop()
