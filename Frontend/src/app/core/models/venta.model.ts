/**
 * Modelo de Venta
 * Representa una venta realizada en el sistema
 */
export interface Venta {
  id: number;
  numero: string;
  fecha: Date;
  clienteId?: number;
  cliente?: Cliente;
  usuarioId: number;
  usuario: string;
  items: VentaItem[];
  subtotal: number;
  descuento: number;
  impuesto: number;
  total: number;
  metodoPago: MetodoPago;
  estado: EstadoVenta;
  cajaId: number;
  observaciones?: string;
}

export interface VentaItem {
  id?: number;
  productoId: number;
  producto: string;
  cantidad: number;
  precioUnitario: number;
  descuento: number;
  subtotal: number;
  iva: number;
  total: number;
}

export interface Cliente {
  id: number;
  nombre: string;
  apellido: string;
  documento: string;
  tipoDocumento: string;
  telefono?: string;
  email?: string;
  direccion?: string;
  ciudad?: string;
  fechaNacimiento?: Date;
  puntosFidelidad: number;
  activo: boolean;
  fechaRegistro: Date;
}

export interface Promocion {
  id: number;
  nombre: string;
  descripcion: string;
  tipo: 'PORCENTAJE' | 'MONTO_FIJO' | '2X1' | '3X2';
  valor: number;
  fechaInicio: Date;
  fechaFin: Date;
  productoIds: number[];
  categoriaIds?: number[];
  activo: boolean;
}

export type MetodoPago = 'EFECTIVO' | 'TARJETA_DEBITO' | 'TARJETA_CREDITO' | 'TRANSFERENCIA' | 'QR';
export type EstadoVenta = 'COMPLETADA' | 'CANCELADA' | 'PENDIENTE';
