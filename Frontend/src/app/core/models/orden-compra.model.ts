
export interface OrdenCompra {
  id: number;
  numero: string;
  fecha: Date;
  fechaEntregaEstimada?: Date;
  proveedorId: number;
  proveedor: string;
  usuarioId: number;
  usuario: string;
  items: OrdenCompraItem[];
  subtotal: number;
  impuesto: number;
  total: number;
  estado: EstadoOrden;
  observaciones?: string;
  fechaCreacion: Date;
  fechaActualizacion?: Date;
}

export interface OrdenCompraItem {
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

export interface OrdenCompraCreateRequest {
  proveedorId: number;
  fechaEntregaEstimada?: Date;
  items: OrdenCompraItemRequest[];
  observaciones?: string;
}

export interface OrdenCompraItemRequest {
  productoId: number;
  cantidad: number;
  precioUnitario: number;
  descuento?: number;
}

export type EstadoOrden = 'PENDIENTE' | 'APROBADA' | 'RECIBIDA' | 'PARCIAL' | 'CANCELADA';
