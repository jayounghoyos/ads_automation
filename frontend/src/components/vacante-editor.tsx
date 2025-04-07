"use client"

import { useState } from "react"
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerDescription,
  DrawerFooter,
  DrawerClose,
} from "@/components/ui/drawer"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"

type Vacante = {
  job_id: number
  titulo: string
  empresa: string
  ubicacion: string
  salario: string
}

interface Props {
  vacante: Vacante
  onClose: () => void
  onSave: (v: Vacante) => void
}

export function VacanteEditor({ vacante, onClose, onSave }: Props) {
  const [formData, setFormData] = useState<Vacante>({ ...vacante })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  return (
    <Drawer open={true} onClose={onClose}>
      <DrawerContent className="p-6 w-full max-w-md mx-auto">
        <DrawerHeader>
          <DrawerTitle>Editar vacante</DrawerTitle>
          <DrawerDescription>Puedes actualizar los campos aquí.</DrawerDescription>
        </DrawerHeader>

        <div className="space-y-4 px-4">
          <div>
            <Label htmlFor="titulo">Título</Label>
            <Input name="titulo" value={formData.titulo} onChange={handleChange} />
          </div>

          <div>
            <Label htmlFor="empresa">Empresa</Label>
            <Input name="empresa" value={formData.empresa} onChange={handleChange} />
          </div>

          <div>
            <Label htmlFor="ubicacion">Ubicación</Label>
            <Input name="ubicacion" value={formData.ubicacion} onChange={handleChange} />
          </div>

          <div>
            <Label htmlFor="salario">Salario</Label>
            <Input name="salario" value={formData.salario} onChange={handleChange} />
          </div>
        </div>

        <DrawerFooter className="mt-4">
          <Button onClick={() => onSave(formData)}>Guardar</Button>
          <Button variant="secondary" onClick={() => setFormData({ ...vacante })}>Resetear</Button>
          <DrawerClose asChild>
            <Button variant="ghost" onClick={onClose}>Cancelar</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  )
}
