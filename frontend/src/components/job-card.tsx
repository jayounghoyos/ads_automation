import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

type Vacante = {
  job_id: number
  titulo: string
  empresa: string
  ubicacion: string
  salario: string
}

type Props = {
  vacante: Vacante
  onPublicar: (id: number) => void
  onEliminar: (id: number) => void
  onDetalle: (v: Vacante) => void // ✅ NUEVO
}

export function JobCard({ vacante, onPublicar, onEliminar, onDetalle }: Props) {
  return (
    <Card>
      <CardContent className="p-4 space-y-2">
        <div className="font-semibold text-lg">{vacante.titulo}</div>
        <div className="text-sm text-muted-foreground">
          {vacante.empresa} — {vacante.ubicacion}
        </div>
        <div className="text-sm">💰 {vacante.salario}</div>
        <div className="flex gap-2 mt-2">
          <Button onClick={() => onDetalle(vacante)}>Ver detalle</Button> {/* ✅ FIX */}
          <Button onClick={() => onPublicar(vacante.job_id)}>Publicar en X</Button>
          <Button variant="destructive" onClick={() => onEliminar(vacante.job_id)}>Eliminar</Button>
        </div>
      </CardContent>
    </Card>
  )
}
