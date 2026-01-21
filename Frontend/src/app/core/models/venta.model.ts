
export interface Venta {
  id: string; // UUID
  sale_number?: string;
  sale_date?: Date;
  created_at?: Date;
  customer_id?: string;
  customer?: Cliente;
  customer_name?: string;
  cashier_id?: string;
  user_id?: string;
  user_name?: string;
  seller_name?: string;
  subtotal: number;
  discount_amount?: number;
  tax_amount?: number;
  total_amount: number;
  total?: number;
  status: string;
  estado?: string;
  notes?: string;
  items?: VentaItem[];
  [key: string]: any; // Para propiedades adicionales del backend
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
  id: string; // UUID
  document_type?: string;
  document_number?: string;
  first_name: string;
  last_name: string;
  business_name?: string;
  email?: string;
  phone?: string;
  address?: string;
  city?: string;
  preferred_contact_method?: string;
  segment: string;
  loyalty_points: number;
  notes?: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
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
