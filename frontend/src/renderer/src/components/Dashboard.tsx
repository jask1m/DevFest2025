import LogStore from "./LogStore"

interface DashboardProps {
  useCase: string
}

export default function Main({ useCase }: DashboardProps) {
  return (
    <div className="flex flex-col h-screen min-w-screen">
      {/* Header */}
      {/* <header className="w-full h-16 flex items-center justify-center bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"> */}
      {/*   <h1 className="text-2xl font-bold">Gloq</h1> */}
      {/* </header> */}
      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden w-full">
        {/* Dashboard */}
        <LogStore />
        {/* Right Panel */}
        <div className="flex-1 p-6">
          <div className="h-full border-2 border-red-500 rounded-lg p-4">{useCase}</div>
        </div>
      </div>
    </div>
  )
}
