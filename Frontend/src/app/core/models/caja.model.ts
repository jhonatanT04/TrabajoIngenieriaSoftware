/**
 * Modelo de Caja
 * Representa las operaciones de caja del sistema
 */
export interface Caja {
  id: number;
  numero: string;
  nombre: string;
  estado: EstadoCaja;
  usuarioId?: number;
  usuario?: string;
  fechaApertura?: Date;
  fechaCierre?: Date;
  montoApertura: number;
  montoCierre?: number;
  totalVentas?: number;
  totalEfectivo?: number;
  totalTarjeta?: number;
  totalOtros?: number;
  observaciones?: string;
}

export interface MovimientoCaja {
  id: number;
  cajaId: number;
  tipo: TipoMovimientoCaja;
  monto: number;
  concepto: string;
  usuarioId: number;
  usuario: string;
  fecha: Date;
  comprobante?: string;
}

export interface ArqueoCaja {
  id: number;
  cajaId: number;
  fecha: Date;
  usuarioId: number;
  usuario: string;
  montoEsperado: number;
  montoContado: number;
  diferencia: number;
  observaciones?: string;
  detalleEfectivo: DetalleEfectivo;
}

export interface DetalleEfectivo {
  billetes200: number;
  billetes100: number;
  billetes50: number;
  billetes20: number;
  billetes10: number;
  monedas5: number;
  monedas2: number;
  monedas1: number;
  monedas05: number;
  total: number;
}

export type EstadoCaja = 'ABIERTA' | 'CERRADA' | 'INACTIVA';
export type TipoMovimientoCaja = 'INGRESO' | 'EGRESO' | 'APERTURA' | 'CIERRE';
