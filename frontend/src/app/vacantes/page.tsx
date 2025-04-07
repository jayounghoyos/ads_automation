"use client"

import { useEffect, useState } from "react"
import { JobCard } from "@/components/job-card"
import { VacanteEditor } from "@/components/vacante-editor"

type Vacante = {
  job_id: number
  titulo: string
  empresa: string
  ubicacion: string
  salario: string
}

export default function VacantesPage() {
  const [vacantes, setVacantes] = useState<Vacante[]>([])
  const [loading, setLoading] = useState(true)
  const [vacanteSeleccionada, setVacanteSeleccionada] = useState<Vacante | null>(null)

  useEffect(() => {
    fetch("http://127.0.0.1:8000/vacantes/")
      .then(res => res.json())
      .then(data => {
        setVacantes(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const publicarEnX = async (id: number) => {
    const res = await fetch("http://127.0.0.1:8000/publicar/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ vacancies: [{ job_id: id }] })
    })

    if (res.ok) {
      const resultado = await res.json()
      alert(`✅ ${resultado.mensaje || "Vacante publicada con éxito"}`)
    } else {
      alert("❌ Error al publicar")
    }
  }

  const eliminarVacante = async (id: number) => {
    const res = await fetch(`http://127.0.0.1:8000/vacantes/${id}`, {
      method: "DELETE"
    })
    if (res.ok) {
      setVacantes(prev => prev.filter(v => v.job_id !== id))
      alert("🗑️ Vacante eliminada")
    } else {
      alert("❌ No se pudo eliminar")
    }
  }

  const actualizarVacante = async (updated: Vacante) => {
    const res = await fetch(`http://127.0.0.1:8000/vacantes/${updated.job_id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated)
    })

    if (res.ok) {
      setVacantes(prev =>
        prev.map(v => v.job_id === updated.job_id ? updated : v)
      )
      setVacanteSeleccionada(null)
      alert("✅ Vacante actualizada")
    } else {
      alert("❌ Error al actualizar")
    }
  }

  return (
    <div className="relative">
      <div className="p-6 max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Vacantes disponibles</h1>
        {loading ? (
          <p>Cargando vacantes...</p>
        ) : (
          <div className="space-y-4">
            {vacantes.map((v) => (
              <JobCard
                key={v.job_id}
                vacante={v}
                onPublicar={publicarEnX}
                onEliminar={eliminarVacante}
                onDetalle={() => setVacanteSeleccionada(v)} // 👈 Nuevo
              />
            ))}
          </div>
        )}
      </div>

      {vacanteSeleccionada && (
        <VacanteEditor
          vacante={vacanteSeleccionada}
          onClose={() => setVacanteSeleccionada(null)}
          onSave={actualizarVacante}
        />
      )}
    </div>
  )
}
