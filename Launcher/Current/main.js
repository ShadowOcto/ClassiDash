const { app, BrowserWindow, ipcMain } = require('electron');
const {shell} = require('electron')
const {download} = require("electron-dl");

app.commandLine.appendSwitch ("disable-http-cache");

function createWindow() {
    const win = new BrowserWindow({
        width: 900,
        height: 550,
        icon: __dirname + '/icon.ico',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    ipcMain.handle('open-path', (req, path) => {
        shell.openPath(path);
    })

    ipcMain.handle('open-url', (req, url) => {
        shell.openExternal(url);
    })
    
    ipcMain.handle('run', (req, exec) => {
        require("child_process").exec(exec)
    })

    ipcMain.on("download", (event, info) => {
        info.properties.onProgress = status => win.webContents.send("download progress", status);
        download(BrowserWindow.getFocusedWindow(), info.url, info.properties)
            .then(dl => win.webContents.send("download complete", dl.getSavePath()));
    });

    // win.setMenu(null);
    win.loadFile('src/index.html');

    win.on('closed', () => {
        app.quit();
    });
}

app.whenReady().then(createWindow);

app.on('window-app-closed', () => {
    app.quit();
});