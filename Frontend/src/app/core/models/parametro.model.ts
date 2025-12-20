
export interface Parametro {
  id: number;
  codigo: string;
  nombre: string;
  valor: string;
  tipo: TipoParametro;
  grupo: GrupoParametro;
  descripcion?: string;
  editable: boolean;
}

export interface ConfiguracionImpuesto {
  id: number;
  nombre: string;
  porcentaje: number;
  aplicaPorDefecto: boolean;
  activo: boolean;
}

export interface ConfiguracionMoneda {
  id: number;
  codigo: string;
  nombre: string;
  simbolo: string;
  esPrincipal: boolean;
  tasaCambio: number;
}

export interface ConfiguracionFormato {
  id: number;
  tipo: 'FACTURA' | 'TICKET' | 'ETIQUETA';
  formato: string;
  plantilla: string;
  activo: boolean;
}

export interface ConfiguracionDescuento {
  id: number;
  nombre: string;
  tipo: 'PORCENTAJE' | 'MONTO_FIJO';
  valor: number;
  requiereAutorizacion: boolean;
  activo: boolean;
}

export interface ConfiguracionGeneral {
  nombreNegocio: string;
  ruc: string;
  direccion: string;
  telefono: string;
  email: string;
  logo?: string;
  impuestos: ConfiguracionImpuesto[];
  monedas: ConfiguracionMoneda[];
  formatoFactura: string;
  requiereAutorizacionDescuento: boolean;
  descuentoMaximoSinAutorizacion: number;
  stockBajoAlerta: boolean;
  puntosPorCompra: number;
  valorPunto: number;
}

export type TipoParametro = 'TEXTO' | 'NUMERO' | 'BOOLEANO' | 'FECHA' | 'JSON';
export type GrupoParametro = 'GENERAL' | 'IMPUESTOS' | 'MONEDA' | 'FORMATO' | 'DESCUENTOS' | 'FIDELIDAD';
