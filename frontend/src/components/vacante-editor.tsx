"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

type Vacante = {
  job_id: number
  titulo: string
  empresa: string
  ubicacion: string
  salario: string
  descripcion: string
}

interface Props {
  vacante: Vacante
  onClose: () => void
  onSave: (v: Vacante) => void
}

export function VacanteEditor({ vacante, onClose, onSave }: Props) {
  const [formData, setFormData] = useState<Vacante>({ ...vacante })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  return (
    <div className="space-y-4 w-full">
      <h2 className="text-xl font-bold">Editar vacante</h2>

      <div className="space-y-2">
        <Label htmlFor="titulo">Título</Label>
        <Input name="titulo" value={formData.titulo} onChange={handleChange} />
      </div>

      <div className="space-y-2">
        <Label htmlFor="empresa">Empresa</Label>
        <Input name="empresa" value={formData.empresa} onChange={handleChange} />
      </div>

      <div className="space-y-2">
        <Label htmlFor="ubicacion">Ubicación</Label>
        <Input name="ubicacion" value={formData.ubicacion} onChange={handleChange} />
      </div>

      <div className="space-y-2">
        <Label htmlFor="salario">Salario</Label>
        <Input name="salario" value={formData.salario} onChange={handleChange} />
      </div>

      <div className="space-y-2">
        <Label htmlFor="descripcion">Descripción</Label>
        <Textarea
          name="descripcion"
          value={formData.descripcion}
          onChange={handleChange}
          className="h-40 resize-y"
        />
      </div>

      <div className="flex gap-2 pt-4">
        <Button onClick={() => onSave(formData)}>Guardar</Button>
        <Button variant="secondary" onClick={() => setFormData({ ...vacante })}>
          Resetear
        </Button>
        <Button variant="ghost" onClick={onClose}>Cancelar</Button>
      </div>
    </div>
  )
}
