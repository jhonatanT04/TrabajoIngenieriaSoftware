
export interface Producto {
  id: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
  categoriaId: number;
  categoria: Categoria;
  precio: number;
  precioCompra: number;
  stock: number;
  stockMinimo: number;
  stockMaximo: number;
  unidadMedida: string;
  imagen?: string;
  activo: boolean;
  proveedorId?: number;
  proveedor?: Proveedor;
  iva: number;
  descuento?: number;
  fechaCreacion: Date;
  fechaActualizacion?: Date;
}

export interface Categoria {
  id: number;
  nombre: string;
  descripcion?: string;
  activo: boolean;
  orden?: number;
  icono?: string;
}

export interface Proveedor {
  id: number;
  nombre: string;
  razonSocial: string;
  ruc: string;
  telefono: string;
  email: string;
  direccion: string;
  ciudad: string;
  contacto: string;
  activo: boolean;
}

export interface ProductoCreateRequest {
  codigo: string;
  nombre: string;
  descripcion?: string;
  categoriaId: number;
  precio: number;
  precioCompra: number;
  stock: number;
  stockMinimo: number;
  stockMaximo: number;
  unidadMedida: string;
  proveedorId?: number;
  iva: number;
}
