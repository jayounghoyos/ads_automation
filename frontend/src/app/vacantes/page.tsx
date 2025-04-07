"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"

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
      body: JSON.stringify({ vacancies: [{ job_id: id }] })  // 👈 Corrección aquí
    });
  
    if (res.ok) {
      const resultado = await res.json();
      alert(`✅ ${resultado.mensaje || "Vacante publicada con éxito"}`);
    } else {
      alert("❌ Error al publicar");
    }
  };
  

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

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Vacantes disponibles</h1>
      {loading ? (
        <p>Cargando vacantes...</p>
      ) : (
        <ul className="space-y-4">
          {vacantes.map((v) => (
            <li key={v.job_id} className="border rounded-lg p-4 shadow-sm">
              <div className="font-semibold text-lg">{v.titulo}</div>
              <div className="text-sm text-gray-500">{v.empresa} - {v.ubicacion}</div>
              <div className="text-sm mt-1">💰 {v.salario}</div>
              <div className="flex gap-2 mt-3">
                <Button onClick={() => alert("Aquí iría el detalle")}>Ver detalle</Button>
                <Button onClick={() => publicarEnX(v.job_id)}>Publicar en X</Button>
                <Button variant="destructive" onClick={() => eliminarVacante(v.job_id)}>Eliminar</Button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
