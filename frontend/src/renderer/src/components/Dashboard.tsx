import LogStore from "./LogStore"
import SearchPanel from "./search-panel"
import PacketChart from "./PacketChart"

interface DashboardProps {
  useCase: string
}

export default function Main({ useCase }: DashboardProps) {
  return (
    <div className="flex flex-col h-screen min-w-screen bg-black">
      {/* Header Bar */}

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden w-full">
        {/* Dashboard */}
        <LogStore />

        {/* Right Panel */}
        <div className="flex-1 flex flex-col py-4 px-2 text-white">
          {/* Top Half - Search Panel */}
          <div className="flex-1 mb-4 rounded-lg border border-zinc-800 bg-zinc-900 p-4">
            <SearchPanel />
          </div>

          {/* Bottom Half */}
          <div className="flex-1 rounded-lg border border-zinc-800 bg-zinc-900 p-4">{useCase}</div>
        </div>
      </div>
    </div>
  )
}
