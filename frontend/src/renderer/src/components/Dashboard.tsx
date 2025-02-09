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
        {/* Left Column - Fixed width */}
        <div className="w-1/2 flex-shrink-0 flex flex-col">
          {/* Log Dashboard */}
          <div className="flex-1 overflow-hidden">
            <LogStore />
          </div>
          
          {/* Chart Section */}
          <div className="h-[25vh] flex-shrink-0">
            <PacketChart />
          </div>
        </div>

        {/* Right Column - Search Panel with fixed width */}
        <div className="w-1/2 flex-shrink-0 flex flex-col py-4 px-2">
          {/* Search Panel Container */}
          <div className="flex-1 mb-4 rounded-lg border border-zinc-800 bg-zinc-900 p-4 overflow-hidden">
            {/* Inner scroll container */}
            <div className="h-full w-full overflow-x-hidden overflow-y-auto">
              <SearchPanel />
            </div>
          </div>
          
          {/* Use Case Label */}
          <div className="h-16 flex-shrink-0 rounded-lg border border-zinc-800 bg-zinc-900 p-4 text-white">
            <span className="font-semibold">Real-Time Analysis:</span> {useCase}
          </div>
        </div>
      </div>
    </div>
  )
}
