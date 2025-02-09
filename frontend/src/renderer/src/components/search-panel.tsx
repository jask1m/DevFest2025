import { useState } from "react"
import { Search } from "lucide-react"

export default function SearchPanel() {
  const [query, setQuery] = useState("")
  const [result, setResult] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    // Simulate a database query with a timeout
    // Replace this with your actual database query
    setResult("Loading...")
    await new Promise((resolve) => setTimeout(resolve, 1000))
    setResult(`Results for query: "${query}"`)
  }

  return (
    <div className="flex flex-col h-full">
      {/* Search Form */}
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search or ask anything..."
            className="w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2 pl-10 pr-4 text-zinc-100 placeholder-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
          />
        </div>
      </form>

      {/* Results Area */}
      <div className="flex-1 overflow-auto rounded-lg border border-zinc-800 bg-zinc-900/50 p-4">
        {result && <p className="text-zinc-100">{result}</p>}
      </div>
    </div>
  )
}
