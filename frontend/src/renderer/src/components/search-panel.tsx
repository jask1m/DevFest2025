import { useState, useEffect, useRef } from "react"
import { Search, Mic, Square } from "lucide-react"
import { Button } from "./ui/button"
import mermaid from 'mermaid'


// Initialize mermaid config (keeping existing config)
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: 'basis',
    nodeSpacing: 80,
    rankSpacing: 100,
    padding: 20,
  },
});

// Helper function to format response (keeping existing function)
function formatResponse(text: string): string {
  const paragraphs = text.split("\n\n")
  return paragraphs
    .map(para => {
      if (para.match(/^\d+\./)) {
        return para.split("\n")
          .map(line => line.trim())
          .join("\n")
      }
      return para.trim()
    })
    .join("\n\n")
}

export default function SearchPanel() {
  const [query, setQuery] = useState("")
  const [result, setResult] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [diagram, setDiagram] = useState<string | null>(null)
  const [isGeneratingDiagram, setIsGeneratingDiagram] = useState(false)
  
  // New voice-related states
  const [isRecording, setIsRecording] = useState(false)
  const [recordingStatus, setRecordingStatus] = useState("")
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])

  // Handle voice recording start
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' })
        
        // Create form data for API request
        const formData = new FormData()
        formData.append('file', audioFile)
        formData.append('model', 'whisper-large-v3-turbo')
        formData.append('language', 'en')
        formData.append('response_format', 'json')
        formData.append('temperature', '0.0')

        try {
          setRecordingStatus("Processing audio...")
          const response = await fetch('https://api.groq.com/openai/v1/audio/transcriptions', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${import.meta.env.VITE_GROQ_API_KEY}`
            },
            body: formData
          })

          if (!response.ok) {
            throw new Error(`API Error: ${response.status}`)
          }

          const data = await response.json()
          if (data.text) {
            setQuery(data.text)
            setRecordingStatus("Transcription successful!")
            // Clear status after a delay
            setTimeout(() => setRecordingStatus(""), 2000)
          } else {
            setRecordingStatus("Error: No transcription found")
          }
        } catch (error) {
          setRecordingStatus(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`)
          console.error('Transcription error:', error)
        }
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
      setRecordingStatus("Recording...")
    } catch (error) {
      setRecordingStatus("Error accessing microphone")
      console.error('Microphone access error:', error)
    }
  }

  // Handle voice recording stop
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      setRecordingStatus("Stopped recording")
      
      // Stop all tracks in the stream
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())
    }
  }

  // Existing generateDiagram function
  async function generateDiagram(text: string) {
    setIsGeneratingDiagram(true)
    try {
      const response = await fetch("http://127.0.0.1:8000/generate-diagram", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ solution: text }),
      })
      if (!response.ok) {
        throw new Error("Failed to generate diagram")
      }
      const data = await response.json()
      setDiagram(data.diagram)
      
      setTimeout(() => {
        mermaid.contentLoaded()
      }, 100)
    } catch (err) {
      console.error("Error generating diagram:", err)
    } finally {
      setIsGeneratingDiagram(false)
    }
  }

  // Existing handleSubmit function
  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsLoading(true)
    setError(null)
    setDiagram(null)
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
      const formattedText = formatResponse(data.response)
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
            className="w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2 pl-10 pr-12 text-zinc-100 placeholder-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
          />
          <button
            type="button"
            onClick={isRecording ? stopRecording : startRecording}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-200 focus:outline-none"
          >
            {isRecording ? (
              <Square className="h-4 w-4" />
            ) : (
              <Mic className="h-4 w-4" />
            )}
          </button>
        </div>
        {recordingStatus && (
          <div className="mt-2 text-sm text-zinc-400">
            {recordingStatus}
          </div>
        )}
      </form>

      {/* Results Area (keeping existing implementation) */}
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
          <div className="text-zinc-100 space-y-4">
            <div className="whitespace-pre-wrap">
              {result.split("\n\n").map((paragraph, idx) => (
                <p key={idx} className="mb-4">
                  {paragraph}
                </p>
              ))}
            </div>
            
            <div className="flex flex-col items-start space-y-4 pt-4 border-t border-zinc-800">
              <Button
                onClick={() => result && generateDiagram(result)}
                disabled={isGeneratingDiagram}
                variant="outline"
                size="sm"
                className="text-zinc-300 hover:text-zinc-100"
              >
                {isGeneratingDiagram ? 'Generating diagram...' : 'Visualize solution diagram'}
              </Button>
              
              {diagram && (
                <div className="w-full bg-zinc-800 rounded-lg p-6 mt-4">
                  <div className="min-h-[600px] flex items-center justify-center">
                    <pre className="mermaid w-full">
                      {diagram}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}