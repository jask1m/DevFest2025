import LogStore from "./LogStore"
import SearchPanel from "./search-panel"
import PacketChart from "./PacketChart"

interface DashboardProps {
  useCase: string
}

export default function Main({ useCase }: DashboardProps) {
  return (
    <div className="flex flex-col h-screen min-w-screen bg-black">
      <div className="flex flex-1 overflow-hidden w-full">
        {/* Left Column */}
        <div className="flex flex-col w-1/2">
          {/* Log Dashboard */}
          <div className="flex-1">
            <LogStore />
          </div>
          
          {/* Chart Section */}
          <div className="h-[25vh]">
            <PacketChart />
          </div>
        </div>

        {/* Right Column - Search Panel */}
        <div className="flex-1 flex flex-col py-4 px-2">
          {/* Search Panel takes most of the space */}
          <div className="flex-1 mb-4 rounded-lg border border-zinc-800 bg-zinc-900 p-4 overflow-y-auto">
            <SearchPanel />
          </div>
          
          {/* Use Case Label */}
          <div className="h-16 rounded-lg border border-zinc-800 bg-zinc-900 p-4 text-white">
            <span className="font-semibold">Real-Time Analysis:</span> {useCase}
          </div>
        </div>
      </div>
    </div>
  )
}

