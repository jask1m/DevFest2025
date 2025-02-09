import { useState } from "react"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { Alert, AlertDescription } from "./ui/alert"
import Dashboard from "./Dashboard"
import GroqLogo from "../assets/gloq_black_long.svg"

export default function Landing() {
  const [useCase, setUseCase] = useState("")
  const [inputValue, setInputValue] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ query: inputValue }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      if (data.error) {
        throw new Error(data.error)
      }
      console.log(data);
      const selected = data["response"]["selected_criteria"];
      const crit = data["response"]["existing_criteria"].filter(x => x.title == selected)[0];
      const scapy_filter = crit["scapy_str"];
      window.electron.ipcRenderer.send('run-with-privileges', scapy_filter);

      setUseCase(inputValue)
    } catch (err: any) {
      if (err.startsWith("Recursion limit")) {
        setError("Please enter a more specific description.")
      } else {
        setError("An error occurred while processing your request")
      }
      console.error("Error:", err)
    } finally {
      setIsLoading(false)
    }
  }

  if (useCase) {
    return <Dashboard useCase={useCase} />
  }

  return (
    <div className="min-w-screen">
    <div className="min-h-screen flex items-center justify-center w-full flex-col bg-gradient-to-b from-zinc-100 via-white to-zinc-100 relative overflow-hidden">
      {/* Animated background effects */}
      <div className="absolute inset-0 overflow-hidden w-screen">
        <div className="absolute -inset-[10px] bg-gradient-to-r from-indigo-200/30 via-purple-200/30 to-indigo-200/30 blur-3xl opacity-50 animate-gradient"></div>
      </div>
      {/* Logo with enhanced animation and light backdrop */}
      <div className="relative mb-7 transform hover:scale-105 transition-transform duration-300 flex justify-center w-full">
        {/* Light backdrop for logo */}
        <div className="absolute inset-0 bg-white/80 blur-xl rounded-full"></div>
        <img 
          src={GroqLogo} 
          alt="Groq Logo"
          className="relative z-10 drop-shadow-xl w-1/2 max-w-md" 
        />
      </div>
      {/* Enhanced Card */}
      <div className="relative w-3/4 mx-4 group">
        {/* Gradient border effect */}
        <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500/50 via-purple-500/50 to-indigo-500/50 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-500"></div>
        <Card className="relative bg-gradient-to-b from-zinc-900 via-zinc-900/95 to-zinc-900 border-indigo-900/20 shadow-2xl">
          <CardHeader>
            <CardTitle className="text-center text-3xl bg-clip-text text-transparent bg-gradient-to-r from-indigo-200 via-indigo-100 to-indigo-200 font-bold">
              Enter network use case to get started
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="relative group">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500/30 via-purple-500/30 to-indigo-500/30 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-300"></div>
                <Input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Enter your use case..."
                  className="relative w-full p-6 bg-gradient-to-r from-zinc-900 via-zinc-900/95 to-zinc-900 border-indigo-900/50 text-indigo-100 placeholder-indigo-300/50 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 shadow-lg transition-all duration-300"
                  disabled={isLoading}
                />
              </div>
              {error && (
                <Alert variant="destructive" className="bg-red-900/10 border-red-900/50 text-red-300">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              <Button 
                type="submit" 
                disabled={isLoading}
                className="w-full p-6 text-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 hover:from-indigo-500 hover:via-purple-500 hover:to-indigo-500 text-white border-0 shadow-lg hover:shadow-indigo-900/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center gap-3">
                    <div className="animate-spin rounded-full h-6 w-6 border-2 border-white/20 border-t-white"></div>
                    Loading...
                  </span>
                ) : (
                  "Submit"
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
      {/* Optional decorative elements - lighter versions */}
      <div className="absolute bottom-0 left-0 w-1/3 h-1/3 bg-indigo-200/20 rounded-full blur-3xl"></div>
      <div className="absolute top-0 right-0 w-1/3 h-1/3 bg-purple-200/20 rounded-full blur-3xl"></div>
    </div>
    </div>
  );
}
