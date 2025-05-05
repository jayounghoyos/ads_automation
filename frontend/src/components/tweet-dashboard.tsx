"use client"

import { useEffect, useState } from "react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LabelList,
} from "recharts"

interface TweetMetric {
  id: string
  texto: string
  likes: number
  retweets: number
  replies: number
  impressions: number
}

export default function TweetDashboard() {
  const [tweets, setTweets] = useState<TweetMetric[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("http://127.0.0.1:8000/tweets/metricas/")
      .then((res) => res.json())
      .then((data) => {
        setTweets(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const totalLikes = tweets.reduce((acc, t) => acc + t.likes, 0)
  const totalRetweets = tweets.reduce((acc, t) => acc + t.retweets, 0)
  const totalReplies = tweets.reduce((acc, t) => acc + t.replies, 0)
  const totalImpressions = tweets.reduce((acc, t) => acc + t.impressions, 0)

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader>
          <CardTitle>❤️ Likes</CardTitle>
          <CardDescription>Total de likes obtenidos</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-3xl font-bold">{totalLikes}</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>🔁 Retweets</CardTitle>
          <CardDescription>Veces compartido</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-3xl font-bold">{totalRetweets}</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>💬 Respuestas</CardTitle>
          <CardDescription>Comentarios recibidos</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-3xl font-bold">{totalReplies}</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>👁️ Impresiones</CardTitle>
          <CardDescription>Total de vistas</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-3xl font-bold">{totalImpressions}</p>
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-2 lg:col-span-4">
        <CardHeader>
          <CardTitle>Actividad por Tweet</CardTitle>
          <CardDescription>Comparativa de likes, retweets y respuestas</CardDescription>
        </CardHeader>
        <CardContent className="pl-2">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={tweets}
              margin={{ top: 16, right: 24, left: 0, bottom: 0 }}
              barCategoryGap={24}
            >
              <XAxis dataKey="id" hide />
              <YAxis />
              <Tooltip />
              <Bar dataKey="likes" name="Likes" fill="#8884d8" radius={[10, 10, 0, 0]} barSize={32}>
                <LabelList dataKey="likes" position="top" />
              </Bar>
              <Bar dataKey="retweets" name="Retweets" fill="#82ca9d" radius={[10, 10, 0, 0]} barSize={32}>
                <LabelList dataKey="retweets" position="top" />
              </Bar>
              <Bar dataKey="replies" name="Respuestas" fill="#ffc658" radius={[10, 10, 0, 0]} barSize={32}>
                <LabelList dataKey="replies" position="top" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}