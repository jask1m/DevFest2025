import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'
let packetDataListener: ((_event: any, data: any) => void) | null = null
// Custom APIs for renderer
const api = {
  onPacketData: (callback: (data: any) => void) => {
    // Remove existing listener if there is one
    if (packetDataListener) {
      ipcRenderer.removeListener('packet-data', packetDataListener)
    }

    // Create new listener
    packetDataListener = (_event: any, data: any) => {
      try {
        if (data) {
          callback(data)
        }
      } catch (error) {
        console.error('Error in packet data callback:', error)
      }
    }

    // Add new listener
    ipcRenderer.on('packet-data', packetDataListener)

    // Return cleanup function
    return () => {
      if (packetDataListener) {
        ipcRenderer.removeListener('packet-data', packetDataListener)
        packetDataListener = null
      }
    }
  },
  removeListeners: () => {
    if (packetDataListener) {
      ipcRenderer.removeListener('packet-data', packetDataListener)
      packetDataListener = null
    }
  }
}

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld('electron', electronAPI)
    contextBridge.exposeInMainWorld('api', api)
  } catch (error) {
    console.error(error)
  }
} else {
  // @ts-ignore (define in dts)
  window.electron = electronAPI
  // @ts-ignore (define in dts)
  window.api = api
}

