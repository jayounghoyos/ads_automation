"use client"

import { useEffect, useState } from "react"

type Recomendacion = {
  usuario: string
  tweet: string
  vacante: string
  empresa: string
}

export default function AnalizarTweets() {
  const [recomendaciones, setRecomendaciones] = useState<Recomendacion[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("http://127.0.0.1:8000/tweets/analisis_local/")
      .then(res => res.json())
      .then(data => {
        // validamos que sea una lista
        if (Array.isArray(data)) {
          setRecomendaciones(data)
        } else {
          console.error("❌ Respuesta inesperada del backend:", data)
        }
        setLoading(false)
      })
      .catch(err => {
        console.error("❌ Error al obtener recomendaciones:", err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Personas buscando empleo</h1>
      {loading ? (
        <p>Analizando tweets con IA...</p>
      ) : (
        <ul className="space-y-4">
          {recomendaciones.map((r, i) => (
            <li key={i} className="border rounded-lg p-4 shadow-sm">
              <p className="font-medium">@{r.usuario}</p>
              <p className="text-sm text-gray-600">📝 {r.tweet}</p>
              <p className="mt-2">🎯 Recomendación: <strong>{r.vacante}</strong> en <strong>{r.empresa}</strong></p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
