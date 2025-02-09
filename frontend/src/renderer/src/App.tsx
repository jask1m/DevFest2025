import { useState } from "react"
import { Button } from "./components/ui/button"
import { Input } from "./components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card"
import Main from "./components/Main"

export default function App() {
  const [useCase, setUseCase] = useState("")
  const [inputValue, setInputValue] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const data = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ use_case: inputValue }),
    })
    const criteria = await data.json()["criteria"]
    console.log("Criteria for llm: ", criteria);
    // at the very end
    setUseCase(inputValue)
  }

  if (useCase) {
    return <Main useCase={useCase} />
  }

  return (
    <div className="min-h-screen flex items-center justify-center w-full">
      <Card className="w-[450px] mx-4">
        <CardHeader>
          <CardTitle className="text-center">Enter network use case to get started</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Enter your use case..."
              className="w-full"
            />
            <Button type="submit" className="w-full">
              Submit
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
