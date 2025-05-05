import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

type Vacante = {
  job_id: number
  titulo: string
  empresa: string
  ubicacion: string
  salario: string
  descripcion: string
}

type Props = {
  vacante: Vacante
  onPublicar: (id: number) => void
  onEliminar: (id: number) => void
  onDetalle: (v: Vacante) => void
}

export function JobCard({ vacante, onPublicar, onEliminar, onDetalle }: Props) {
  return (
    <Card className="text-foreground border border-border shadow-sm">
      <CardContent className="p-4 space-y-2">
        <div className="font-semibold text-lg text-primary">{vacante.titulo}</div>
        <div className="text-sm">
          {vacante.empresa} — {vacante.ubicacion}
        </div>
        <div className="text-sm">💰 {vacante.salario}</div>
        <div className="text-sm text-zinc-500 line-clamp-2">{vacante.descripcion}</div>
        <div className="flex gap-2 mt-2">
          <Button onClick={() => onDetalle(vacante)}>Ver detalle</Button>
          <Button onClick={() => onPublicar(vacante.job_id)}>📤 Publicar</Button>
          <Button variant="destructive" onClick={() => onEliminar(vacante.job_id)}>Eliminar</Button>
        </div>
      </CardContent>
    </Card>
  )
}