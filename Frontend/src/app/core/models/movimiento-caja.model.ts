export interface MovimientoCaja {
  fecha: Date;
  tipo: 'INGRESO' | 'EGRESO';
  descripcion: string;
  monto: number;
}
