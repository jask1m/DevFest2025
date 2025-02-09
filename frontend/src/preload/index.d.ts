import { ElectronAPI } from '@electron-toolkit/preload'

interface API {
  runWithPrivileges(filter: string): void
  onPacketData(callback: (data: Dict) => void): void
  onPythonProcessEnded(callback: (code: number) => void): void
  onPythonProcessError(callback: (error: string) => void): void
  removeAllListeners(): void
}

declare global {
  interface Window {
    electron: ElectronAPI
    api: API
  }
}
