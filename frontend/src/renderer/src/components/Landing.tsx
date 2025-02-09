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
    } catch (err) {
      console.error("Error:", err)
      setError(err instanceof Error ? err.message : "An error occurred while processing your request")
    } finally {
      setIsLoading(false)
    }
  }

  if (useCase) {
    return <Dashboard useCase={useCase} />
  }

  return (
    <div className="min-h-screen flex items-center justify-center w-full flex-col">
      <img src={GroqLogo} width={"50%"} className="mb-7" />
      <Card className="w-3/4 mx-4">
        <CardHeader>
          <CardTitle className="text-center text-3xl">Enter network use case to get started</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Enter your use case..."
              className="w-full p-5"
              disabled={isLoading}
            />
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            <Button type="submit" className="w-full text-2xl p-5" disabled={isLoading}>
              {isLoading ? "Loading..." : "Submit"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
