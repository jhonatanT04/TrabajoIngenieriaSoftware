/**
 * Modelo de Reportes
 * Representa datos y configuraciones para reportes del sistema
 */
export interface ReporteVentas {
  periodo: string;
  totalVentas: number;
  cantidadVentas: number;
  promedioVenta: number;
  ventasPorMetodoPago: VentaPorMetodoPago[];
  ventasPorDia: VentaPorDia[];
  productosMasVendidos: ProductoMasVendido[];
}

export interface VentaPorMetodoPago {
  metodoPago: string;
  cantidad: number;
  monto: number;
  porcentaje: number;
}

export interface VentaPorDia {
  fecha: string;
  cantidad: number;
  monto: number;
}

export interface ProductoMasVendido {
  productoId: number;
  producto: string;
  cantidad: number;
  monto: number;
}

export interface ReporteInventario {
  totalProductos: number;
  valorInventario: number;
  productosStockBajo: ProductoStockBajo[];
  productosStockAlto: ProductoStockAlto[];
  movimientosRecientes: MovimientoResumen[];
}

export interface ProductoStockBajo {
  productoId: number;
  producto: string;
  stock: number;
  stockMinimo: number;
  diferencia: number;
}

export interface ProductoStockAlto {
  productoId: number;
  producto: string;
  stock: number;
  stockMaximo: number;
  diferencia: number;
}

export interface MovimientoResumen {
  fecha: string;
  tipo: string;
  cantidad: number;
}

export interface ReporteCaja {
  periodo: string;
  totalIngresos: number;
  totalEgresos: number;
  saldo: number;
  cajas: CajaResumen[];
}

export interface CajaResumen {
  cajaId: number;
  caja: string;
  aperturas: number;
  totalVentas: number;
  totalEfectivo: number;
  totalTarjeta: number;
}

export interface ReporteClientes {
  totalClientes: number;
  clientesActivos: number;
  clientesNuevos: number;
  topClientes: ClienteTop[];
  puntosFidelidad: ResumenPuntos;
}

export interface ClienteTop {
  clienteId: number;
  cliente: string;
  totalCompras: number;
  montoTotal: number;
}

export interface ResumenPuntos {
  totalPuntosOtorgados: number;
  totalPuntosCanjeados: number;
  puntosVigentes: number;
}

export interface FiltroReporte {
  fechaInicio: Date;
  fechaFin: Date;
  tipo?: string;
  categoriaId?: number;
  proveedorId?: number;
  usuarioId?: number;
}
