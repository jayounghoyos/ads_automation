"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"

interface Vacante {
  job_id: number
  titulo: string
  empresa: string
  ubicacion: string
  salario: string
}

interface Props {
  vacantes: Vacante[]
  ciudad: string
  setCiudad: (val: string) => void
  salarioMin: number
  setSalarioMin: (val: number) => void
  salarioMax: number
  setSalarioMax: (val: number) => void
}

export function PublicacionTools({
  vacantes,
  ciudad,
  setCiudad,
  salarioMin,
  setSalarioMin,
  salarioMax,
  setSalarioMax
}: Props) {
  const publicarTodas = async () => {
    const ids = vacantes.map(v => ({ job_id: v.job_id }))
    const res = await fetch("http://127.0.0.1:8000/publicar/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ vacancies: ids })
    })
    alert(res.ok ? "✅ Publicadas todas" : "❌ Error al publicar")
  }

  const publicarSegmentado = async () => {
    const filtradas = vacantes.filter(v => {
      const salarioNum = parseInt(v.salario.replace(/[^\d]/g, ""))
      const matchSalario = salarioNum >= salarioMin && salarioNum <= salarioMax
      const matchCiudad = ciudad ? v.ubicacion.toLowerCase().includes(ciudad.toLowerCase()) : true
      return matchSalario && matchCiudad
    })
    if (filtradas.length === 0) return alert("⚠️ No hay vacantes que cumplan los criterios")

    const res = await fetch("http://127.0.0.1:8000/publicar/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ vacancies: filtradas.map(v => ({ job_id: v.job_id })) })
    })
    alert(res.ok ? `✅ Publicadas ${filtradas.length} vacantes` : "❌ Error al publicar")
  }

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Acciones</h2>

      <Button className="w-full" onClick={publicarTodas}>
        📢 Publicar todas
      </Button>

      <Collapsible>
        <CollapsibleTrigger asChild>
          <Button variant="outline" className="w-full">
            🎯 Publicar segmentado
          </Button>
        </CollapsibleTrigger>

        <CollapsibleContent className="space-y-4 mt-4">
          <div className="space-y-2">
            <Label htmlFor="salarioMin">Salario mínimo (x1000 dolares)</Label>
            <Input
              type="number"
              value={salarioMin}
              onChange={e => setSalarioMin(Number(e.target.value))}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="salarioMax">Salario máximo (x1000 dolares)</Label>
            <Input
              type="number"
              value={salarioMax}
              onChange={e => setSalarioMax(Number(e.target.value))}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="ciudad">Ciudad</Label>
            <Input
              value={ciudad}
              onChange={e => setCiudad(e.target.value)}
            />
          </div>

          <Button className="w-full" variant="secondary" onClick={publicarSegmentado}>
            🚀 Ejecutar publicación segmentada
          </Button>
        </CollapsibleContent>
      </Collapsible>
    </div>
  )
}