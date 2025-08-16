"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Sparkles, Mail } from "lucide-react"

interface Recomendacion {
  usuario?: string
  tweet?: string
  vacante?: string
  empresa?: string
}

export default function AnalizarPage() {
  const [recomendaciones, setRecomendaciones] = useState<Recomendacion[]>([])
  const [loading, setLoading] = useState(false)
  const searchParams = useSearchParams()
  const modo = searchParams.get("modo") // "ia" o "local"

  useEffect(() => {
    if (!modo) return

    const endpoint =
      modo === "local"
        ? "http://localhost:8000/tweets/analisis_local/"
        : "http://localhost:8000/analizar/"

    setLoading(true)
    fetch(endpoint)
      .then((res) => res.json())
      .then((data) => {
        setRecomendaciones(data.recomendaciones || data)
        setLoading(false)
      })
      .catch((err) => {
        console.error("Error al obtener recomendaciones:", err)
        setLoading(false)
      })
  }, [modo])

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-4">
        {modo === "local" ? "Análisis Local" : "Análisis con IA"}
      </h1>

      {loading && <p>Cargando análisis...</p>}
      {!loading && recomendaciones.length === 0 && <p>No hay recomendaciones.</p>}

      <div className="grid gap-4">
        {recomendaciones.map((rec: Recomendacion, index: number) => (
          <Card key={index} className="bg-white dark:bg-zinc-900 shadow">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-blue-500" />
                {typeof rec === "string" ? rec : `@${rec.usuario}`}
              </CardTitle>
            </CardHeader>
            {typeof rec !== "string" && (
              <CardContent className="text-sm text-zinc-600 dark:text-zinc-300 space-y-2">
                <p className="break-words">📝 {rec.tweet}</p>
                <p className="font-medium flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-pink-500" />
                  Recomendación:
                  <span className="text-zinc-900 dark:text-white font-semibold ml-1">
                    {rec.vacante}
                  </span>{" "}
                  en{" "}
                  <span className="text-zinc-900 dark:text-white font-semibold">
                    {rec.empresa}
                  </span>
                </p>
              </CardContent>
            )}
          </Card>
        ))}
      </div>
    </div>
  )
}
