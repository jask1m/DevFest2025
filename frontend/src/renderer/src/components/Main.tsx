interface MainProps {
  useCase: string
}

export default function Main({ useCase }: MainProps) {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Selected Use Case: {useCase}</h1>
      {/* Add your main component content here */}
    </div>
  )
}

