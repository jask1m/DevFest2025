import { useState } from "react"
import { Search } from "lucide-react"

// Helper function to format the markdown-like response
function formatResponse(text: string): string {
  // Split into paragraphs
  const paragraphs = text.split("\n\n")
  
  // Process each paragraph
  return paragraphs
    .map(para => {
      // Handle numbered lists
      if (para.match(/^\d+\./)) {
        return para.split("\n")
          .map(line => line.trim())
          .join("\n")
      }
      // Handle regular paragraphs
      return para.trim()
    })
    .join("\n\n")
}

export default function SearchPanel() {
  const [query, setQuery] = useState("")
  const [result, setResult] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ query: query }),
      })

      if (!response.ok) {
        throw new Error("Failed to fetch results")
      }

      const data = await response.json()
      
      // Format the response text
      const formattedText = formatResponse(data.response)
      console.log(formattedText);
      setResult(formattedText)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
      setResult(null)
    } finally {
      setIsLoading(false)
    }
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
        {isLoading && (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-zinc-400"></div>
          </div>
        )}
        
        {error && (
          <p className="text-red-400">{error}</p>
        )}
        
        {result && !isLoading && (
          <div className="text-zinc-100 whitespace-pre-wrap">
            {result.split("\n\n").map((paragraph, idx) => (
              <p key={idx} className="mb-4">
                {paragraph}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}