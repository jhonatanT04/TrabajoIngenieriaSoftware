
export interface Producto {
  id?: string; // UUID del backend
  sku: string;
  barcode?: string;
  name: string;
  description?: string;
  category_id?: string;
  category?: Categoria;
  brand_id?: string;
  brand?: Brand;
  main_supplier_id?: string;
  supplier?: Proveedor;
  unit_of_measure: string;
  sale_price: number;
  cost_price: number;
  tax_rate: number;
  stock_min: number;
  stock_max?: number;
  weight?: number;
  requires_lot_control: boolean;
  requires_expiration_date: boolean;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface Categoria {
  id: string;
  name: string;
  description?: string;
  parent_category_id?: string;
  created_at?: string;
}

export interface Brand {
  id: string;
  name: string;
  description?: string;
}

export interface Proveedor {
  id: string;
  business_name: string;
  tax_id?: string;
  contact_name?: string;
  email?: string;
  phone?: string;
  address?: string;
  city?: string;
  country?: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface ProductoCreateRequest {
  sku: string;
  name: string;
  description?: string;
  category_id?: string;
  brand_id?: string;
  main_supplier_id?: string;
  unit_of_measure: string;
  sale_price: number;
  cost_price: number;
  tax_rate: number;
  stock_min: number;
  stock_max?: number;
  is_active?: boolean;
}
