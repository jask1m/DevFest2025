import LogStore from "./LogStore"

interface DashboardProps {
  useCase: string
}

export default function Main({ useCase }: DashboardProps) {
  return (
    <div className="flex flex-col h-screen min-w-screen bg-black">
      {/* Header */}
      {/* <header className="w-full h-16 flex items-center justify-center bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"> */}
      {/*   <h1 className="text-2xl font-bold">Gloq</h1> */}
      {/* </header> */}
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

