import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "./ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "./ui/chart"

interface PacketData {
  time: string
  packets: number
}

interface PacketChartProps {
  data?: PacketData[]
  title?: string
  className?: string
}

// Chart configuration
const chartConfig = {
  packets: {
    label: "Packets",
    color: "hsl(var(--chart-1))",
  },
} satisfies ChartConfig

// Default sample data generator with explicit typing
const generateSampleData = (): PacketData[] => {
  const data: PacketData[] = []
  for (let i = 0; i < 30; i++) {
    const packetData: PacketData = {
      time: `${i * 10}s`,
      packets: Math.floor(Math.random() * 500)
    }
    data.push(packetData)
  }
  return data
}

const PacketChart = ({
  data = generateSampleData(),
  title = "Network Traffic",
  className = ""
}: PacketChartProps) => {
  return (
    <div className="px-2">
      <Card className={`border-zinc-800 bg-zinc-900 text-white ${className}`}>
        <CardHeader className="border-b border-zinc-800 p-4">
          <CardTitle>{title}</CardTitle>
        </CardHeader>
        <CardContent className="p-4">
          <ChartContainer 
            config={chartConfig}
            className="h-[150px] w-full" // Reduced height from 200px to 150px
          >
            <AreaChart 
              data={data}
              margin={{ top: 5, right: 5, bottom: 5, left: 5 }} // Added consistent margins
            >
              <defs>
                <linearGradient id="fillPackets" x1="0" y1="0" x2="0" y2="1">
                  <stop 
                    offset="5%" 
                    stopColor="var(--color-packets)" 
                    stopOpacity={0.8} 
                  />
                  <stop 
                    offset="95%" 
                    stopColor="var(--color-packets)" 
                    stopOpacity={0.1} 
                  />
                </linearGradient>
              </defs>
              <CartesianGrid 
                vertical={false} 
                stroke="hsl(var(--border))"
                strokeDasharray="3 3"
              />
              <XAxis
                dataKey="time"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                stroke="hsl(var(--foreground))"
                tick={{ fill: 'hsl(var(--foreground))' }}
              />
              <YAxis
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                stroke="hsl(var(--foreground))"
                tick={{ fill: 'hsl(var(--foreground))' }}
                label={{ 
                  value: 'Packets', 
                  angle: -90, 
                  position: 'insideLeft',
                  fill: 'hsl(var(--foreground))',
                  style: { textAnchor: 'middle' }
                }}
              />
              <ChartTooltip
                cursor={false}
                content={<ChartTooltipContent />}
              />
              <Area
                type="monotone"
                dataKey="packets"
                stroke="var(--color-packets)"
                fill="url(#fillPackets)"
                isAnimationActive={true}
                animationDuration={500}
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
      </Card>
    </div>
  )
}

export default PacketChart