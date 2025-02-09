import { useEffect, useState } from "react"
import { CardHeader, CardTitle } from "./ui/card"
import { ScrollArea, ScrollBar } from "./ui/scroll-area"
import { Badge } from "./ui/badge"
import { AlertCircle, ArrowRight } from "lucide-react"

interface NetworkLog {
  id: number,
  timestamp: number,
  type: "info" | "warning" | "error"
  source_mac: string
  destination_mac: string
  source_ip: string
  destination_ip: string,
  ttl: number,
  protocols: string
  message: string
  isMalicious: boolean
}


export default function LogStore() {
  const [logs, setLogs] = useState<NetworkLog[]>([])
  const [count, setCount] = useState(0)
  window.api.onPacketData((data) => {
    data = JSON.parse(data)
    console.log('Received packet data:', data);
    const new_packet: NetworkLog = {
      id: count,
      timestamp: Date.now(),
      type: 'info',
      source_mac: data["Ethernet"]["src"],
      destination_mac: data["Ethernet"]["dst"],
      source_ip: data["IP"]["src"],
      destination_ip: data["IP"]["dst"],
      ttl: data[
        "IP"
      ]["ttl"],
      protocols: Object.keys(data).join(', '),
      message: data,
      isMalicious: false,
    }
    setCount(count + 1);
    setLogs([new_packet, ...logs]);
    console.log(count);
  });
  // useEffect(() => {
  //   const initialLogs = Array(10).fill(null).map(generateMockLog)
  //   setLogs(initialLogs)
  // }, [])

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setLogs((prevLogs) => [generateMockLog(), ...prevLogs])
  //   }, 3000)
  //   return () => clearInterval(interval)
  // }, [])

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
                      className="h-5 font-medium text-white bg-emerald-500"
                    >
                      {log.type === "error" && <AlertCircle className="w-3 h-3 mr-1" />}
                      {log.type.toUpperCase()}
                    </Badge>
                    <Badge
                      variant="outline"
                      className="bg-zinc-900 text-zinc-400 border-zinc-800"
                    >
                      {log.protocols}
                    </Badge>
                    <span className="text-xs text-zinc-500 ml-auto">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                  </div>

                  {/* Address Layout */}
                  <div className="grid grid-cols-7 gap-2">
                    {/* Source Address Column */}
                    <div className="col-span-1">
                      <div className="flex flex-col">
                        {/* Source IP */}
                        <div className="mb-2">
                          <span className="text-zinc-500 text-sm">Source IP</span>
                          <div className="font-mono text-zinc-300 text-sm">{log.source_ip}</div>
                        </div>
                        {/* Source MAC */}
                        <div>
                          <span className="text-zinc-500 text-sm">Source MAC</span>
                          <div className="font-mono text-zinc-300 text-sm">{log.source_mac}</div>
                        </div>
                      </div>
                    </div>

                    {/* Arrow Column */}
                    <div className="col-span-1 flex items-center justify-center">
                      <ArrowRight className="w-6 h-6 text-zinc-600" />
                    </div>

                    {/* Destination Address Column */}
                    <div className="col-span-5">
                      <div className="flex flex-col">
                        {/* Destination IP */}
                        <div className="mb-2">
                          <span className="text-zinc-500 text-sm">Destination IP</span>
                          <div className="font-mono text-zinc-300 text-sm">{log.destination_ip}</div>
                        </div>
                        {/* Destination MAC */}
                        <div>
                          <span className="text-zinc-500 text-sm">Destination MAC</span>
                          <div className="font-mono text-zinc-300 text-sm">{log.destination_mac}</div>
                        </div>
                      </div>
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
