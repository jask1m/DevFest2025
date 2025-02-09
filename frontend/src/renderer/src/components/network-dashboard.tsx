import { useEffect, useState } from "react"
import { CardHeader, CardTitle } from "./ui/card"
import { ScrollArea, ScrollBar } from "./ui/scroll-area"
import { Badge } from "./ui/badge"
import { AlertCircle, ArrowRight } from "lucide-react"

interface NetworkLog {
  id: string
  timestamp: string 
  type: "info" | "warning" | "error"
  source: string
  destination: string
  protocol: string
  message: string
  isMalicious: boolean
}

const generateMockLog = (): NetworkLog => {
  const protocols = ["TCP", "UDP", "HTTP", "HTTPS"]
  const types: Array<"info" | "warning" | "error"> = ["info", "warning", "error"]
  return {
    id: Math.random().toString(36).substr(2, 9),
    timestamp: new Date().toISOString(),
    type: types[Math.floor(Math.random() * types.length)],
    source: `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
    destination: `10.0.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
    protocol: protocols[Math.floor(Math.random() * protocols.length)],
    message: `Packet transferred: ${Math.floor(Math.random() * 1500)} bytes`,
    isMalicious: Math.random() < 0.2,
  }
}

export default function NetworkDashboard() {
  const [logs, setLogs] = useState<NetworkLog[]>([])

  useEffect(() => {
    const initialLogs = Array(10).fill(null).map(generateMockLog)
    setLogs(initialLogs)
  }, [])

  useEffect(() => {
    const interval = setInterval(() => {
      setLogs((prevLogs) => [generateMockLog(), ...prevLogs])
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  const getBadgeVariant = (type: NetworkLog["type"]) => {
    switch (type) {
      case "error":
        return "destructive"
      case "warning":
        return "warning"
      default:
        return "secondary"
    }
  }

  return (
    <div className="w-full max-w-[64rem] py-4 px-2 h-full bg-black">
      <div className="rounded-lg h-full flex flex-col bg-zinc-900 border border-zinc-800">
        <CardHeader className="border-b border-zinc-800 py-4">
          <CardTitle className="text-zinc-100">Network Logs</CardTitle>
        </CardHeader>
        <div className="flex-1 min-h-0">
          <ScrollArea className="h-full">
            <div className="flex flex-col gap-2 p-3">
              {logs.map((log) => (
                <div
                  key={log.id}
                  className={`rounded-lg bg-zinc-950 p-3 
                    ${log.isMalicious 
                      ? 'border-l-4 border-red-500 bg-red-500/5' 
                      : 'border-l-4 border-emerald-500 bg-emerald-500/5'}`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Badge 
                      variant={getBadgeVariant(log.type)} 
                      className="h-5 font-medium"
                    >
                      {log.type === "error" && <AlertCircle className="w-3 h-3 mr-1" />}
                      {log.type.toUpperCase()}
                    </Badge>
                    <Badge 
                      variant="outline" 
                      className="bg-zinc-900 text-zinc-400 border-zinc-800"
                    >
                      {log.protocol}
                    </Badge>
                    <span className="text-xs text-zinc-500 ml-auto">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-12 gap-4 items-center text-sm">
                    <div className="col-span-4 flex items-center gap-2">
                      <span className="text-zinc-500">From:</span>
                      <code className="font-mono text-zinc-300">{log.source}</code>
                    </div>
                    <ArrowRight className="w-4 h-4 text-zinc-600" />
                    <div className="col-span-4 flex items-center gap-2">
                      <span className="text-zinc-500">To:</span>
                      <code className="font-mono text-zinc-300">{log.destination}</code>
                    </div>
                    <div className="col-span-3 flex items-center gap-2">
                      <span className="text-zinc-500">Size:</span>
                      <span className="text-zinc-300">{log.message.split(': ')[1]}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <ScrollBar />
          </ScrollArea>
        </div>
      </div>
    </div>
  )
}