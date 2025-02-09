import { app, shell, BrowserWindow, ipcMain } from 'electron'
import path, { join } from 'path'
import { platform } from 'os'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import { spawn } from 'child_process'
let win: BrowserWindow | null = null;
function parseScapyPacket(dump) {
  const packetDict = {};
  let layer = "Eth";

  dump.toString().split("\n").forEach(line => {
    line = line.trim();

    if (!line) return; // Skip empty lines

    if (line.includes("###")) {
      layer = line.replace(/[#\[\]]/g, "").trim();
      packetDict[layer] = {};
    } else if (line.includes("=") && layer) {
      const [key, val] = line.split("=").map(s => s.trim());
      packetDict[layer][key] = val;
    }
  });

  return JSON.stringify(packetDict, null, 4);
}
async function runWithPrivileges(scapy_filter: string) {
  const isWindows = platform() === 'win32';
  const isMac = platform() === 'darwin';

  // Determine the privilege escalation command based on OS
  let privilegeCommand: string;
  if (isWindows) {
    privilegeCommand = 'pkexec';
  } else if (isMac) {
    privilegeCommand = 'sudo';
  } else {
    // Linux and other Unix-like systems
    privilegeCommand = 'pkexec';
  }
  console.log(`Requesting privileges via pkexec...`);

  const pythonScriptPath = path.join(app.getAppPath(), "python", "logger.py");
  const pythonExecutablePath = path.join(app.getAppPath(), "python", "venv", "bin", "python3")

  const python = spawn(privilegeCommand, [pythonExecutablePath, pythonScriptPath, scapy_filter], {
    stdio: ["inherit", 'pipe', 'pipe']
  });

  python.stdout?.on('data', function (data) {
    const jobj = parseScapyPacket(data)

    console.log(jobj.toString());
    if (win) {
      win.webContents.send('packet-data', jobj);
      console.log("window found")
    }
    else console.log("no window")
  });
  python.on("close", (code) => {
    console.log(`Python process exited with code ${code}`);
    app.quit()
  });

  python.on("error", (err) => {
    console.error(`Failed to start process: ${err}`);
  });
}
function createWindow(): void {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    show: false,
    autoHideMenuBar: true,
    ...(process.platform === 'linux' ? { icon } : {}),
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false,
      contextIsolation: true
    },
  })
  mainWindow.once('ready-to-show', () => {
    mainWindow.maximize();
    mainWindow.show();
  });
  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
  win = mainWindow;
}
// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  // IPC test
  ipcMain.on('ping', () => console.log('pong'))

  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()

  })
  ipcMain.on('run-with-privileges', (event, scapy_filter) => {
    runWithPrivileges(scapy_filter);
  });
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and require them here.
