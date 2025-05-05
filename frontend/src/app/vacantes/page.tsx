"use client"

import { useEffect, useState } from "react"
import { JobCard } from "@/components/job-card"
import { VacanteEditor } from "@/components/vacante-editor"
import { PublicacionTools } from "@/components/publicacion-tools"


// Tipo de datos de cada vacante
type Vacante = {
  job_id: number
  titulo: string
  empresa: string
  ubicacion: string
  salario: string
  descripcion: string
}

export default function VacantesPage() {
  const [vacantes, setVacantes] = useState<Vacante[]>([])
  const [loading, setLoading] = useState(true)
  const [vacanteSeleccionada, setVacanteSeleccionada] = useState<Vacante | null>(null)
  const [ciudadFiltro, setCiudadFiltro] = useState("")
  const [salarioMin, setSalarioMin] = useState(0)
  const [salarioMax, setSalarioMax] = useState(999999)
  const [busqueda, setBusqueda] = useState("")
  const [plataformasSeleccionadas, setPlataformasSeleccionadas] = useState<string[]>([])

  const togglePlataforma = (plataforma: string) => {
    setPlataformasSeleccionadas(prev =>
      prev.includes(plataforma)
        ? prev.filter(p => p !== plataforma)
        : [...prev, plataforma]
    )
  }

  useEffect(() => {
    fetch("http://127.0.0.1:8000/vacantes/")
      .then(res => res.json())
      .then(data => {
        setVacantes(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const publicarVacante = async (id: number) => {
    for (const plataforma of plataformasSeleccionadas) {
      const url =
        plataforma === "x"
          ? "http://127.0.0.1:8000/publicar/"
          : plataforma === "telegram"
          ? "http://127.0.0.1:8000/publicar/telegram/"
          : null
  
      if (!url) continue
  
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ vacancies: [{ job_id: id }] }),
      })
  
      if (!res.ok) {
        alert(`❌ Error al publicar en ${plataforma}`)
      }
    }
  
    alert("✅ Publicación completada")
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

  const vacantesFiltradas = vacantes.filter(v => {
    const salario = parseInt(v.salario.split("-")[0].replace(/[^\d]/g, ""), 10) || 0
    const coincideBusqueda =
      v.titulo.toLowerCase().includes(busqueda.toLowerCase()) ||
      v.empresa.toLowerCase().includes(busqueda.toLowerCase())
  
    return (
      v.ubicacion.toLowerCase().includes(ciudadFiltro.toLowerCase()) &&
      salario >= salarioMin &&
      salario <= salarioMax &&
      coincideBusqueda
    )
  })
  

  return (
    <div className="flex min-h-screen">
      {/* Columna izquierda */}
      <aside className="w-[250px] bg-muted p-4 border-r">
        <PublicacionTools
          vacantes={vacantes}
          ciudad={ciudadFiltro}
          setCiudad={setCiudadFiltro}
          salarioMin={salarioMin}
          setSalarioMin={setSalarioMin}
          salarioMax={salarioMax}
          setSalarioMax={setSalarioMax}
          plataformasSeleccionadas={plataformasSeleccionadas}
          togglePlataforma={togglePlataforma}
        />
      </aside>

      {/* Columna central */}
      <main className="flex-1 p-6 overflow-y-auto">
        <div className="mb-4">
          <h1 className="text-2xl font-bold mb-2">Vacantes disponibles</h1>
          <input
            type="text"
            placeholder="🔍 Buscar por título o empresa"
            className="w-full border border-zinc-300 rounded px-3 py-2 text-sm dark:bg-zinc-800 dark:text-white"
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </div>
        {loading ? (
          <p>Cargando vacantes...</p>
        ) : (
          <div className="space-y-4">
            {vacantesFiltradas.map((v) => (
              <JobCard
                key={v.job_id}
                vacante={v}
                onPublicar={publicarVacante}
                onEliminar={eliminarVacante}
                onDetalle={() => setVacanteSeleccionada(v)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Columna derecha */}
      {vacanteSeleccionada && (
        <aside className="w-[350px] bg-white border-l shadow-inner p-4">
          <VacanteEditor
            vacante={vacanteSeleccionada}
            onClose={() => setVacanteSeleccionada(null)}
            onSave={actualizarVacante}
          />
        </aside>
      )}
    </div>
  )
}