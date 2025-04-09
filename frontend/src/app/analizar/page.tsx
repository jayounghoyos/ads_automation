"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"

export default function AnalizarPage() {
  const [recomendaciones, setRecomendaciones] = useState<any[]>([])
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

      <ul className="space-y-4 mt-4">
        {recomendaciones.map((rec: any, index) => (
          <li key={index} className="bg-white p-4 rounded shadow text-zinc-800 dark:bg-zinc-800 dark:text-white">
            {typeof rec === "string" ? rec : (
              <>
                <strong>@{rec.usuario}</strong> → {rec.vacante} en {rec.empresa}
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
