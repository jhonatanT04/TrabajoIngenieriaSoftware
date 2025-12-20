
export interface MovimientoInventario {
  id: number;
  tipo: TipoMovimientoInventario;
  productoId: number;
  producto: string;
  cantidad: number;
  cantidadAnterior: number;
  cantidadNueva: number;
  motivo: string;
  usuarioId: number;
  usuario: string;
  fecha: Date;
  ordenCompraId?: number;
  recepcionId?: number;
}

export interface RecepcionMercancia {
  id: number;
  numero: string;
  fecha: Date;
  proveedorId: number;
  proveedor: string;
  ordenCompraId?: number;
  usuarioId: number;
  usuario: string;
  items: RecepcionItem[];
  estado: EstadoRecepcion;
  observaciones?: string;
}

export interface RecepcionItem {
  id?: number;
  productoId: number;
  producto: string;
  cantidadEsperada?: number;
  cantidadRecibida: number;
  precioUnitario: number;
  subtotal: number;
  lote?: string;
  fechaVencimiento?: Date;
}

export interface AjusteInventario {
  id: number;
  fecha: Date;
  usuarioId: number;
  usuario: string;
  motivo: string;
  items: AjusteItem[];
  observaciones?: string;
}

export interface AjusteItem {
  productoId: number;
  producto: string;
  stockActual: number;
  stockContado: number;
  diferencia: number;
  motivo: string;
}

export interface Etiqueta {
  productoId: number;
  codigo: string;
  nombre: string;
  precio: number;
  formato: 'PEQUENA' | 'MEDIANA' | 'GRANDE';
}

export type TipoMovimientoInventario = 'ENTRADA' | 'SALIDA' | 'AJUSTE' | 'DEVOLUCION' | 'TRANSFERENCIA';
export type EstadoRecepcion = 'PENDIENTE' | 'RECIBIDA' | 'PARCIAL' | 'CANCELADA';
