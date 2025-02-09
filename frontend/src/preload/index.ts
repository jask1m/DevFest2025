import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'

// Custom APIs for renderer
const api = {}

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld('electron', electronAPI)
    contextBridge.exposeInMainWorld('api', api)
    contextBridge.exposeInMainWorld(
      'api', {
      startSniffer: () => ipcRenderer.invoke('start-sniffer'),
      stopSniffer: () => ipcRenderer.invoke('stop-sniffer'),
      onSnifferData: (callback) => ipcRenderer.on('sniffer-data', callback),
      onSnifferError: (callback) => ipcRenderer.on('sniffer-error', callback)
    }
    );
  } catch (error) {
    console.error(error)
  }
} else {
  // @ts-ignore (define in dts)
  window.electron = electronAPI
  // @ts-ignore (define in dts)
  window.api = api
}

