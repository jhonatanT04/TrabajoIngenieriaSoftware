
export interface Usuario {
  id: string; // UUID en el backend
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  profile_id: string; // UUID
  profile?: Profile;
  profile_name?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  password?: string;
  document_number?: string;
  hashed_password?: string; // Solo para creación, no se retorna en GET
}

export interface Profile {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;
  permissions?: Permission[];
}

export interface Permission {
  id: string;
  module_name: string;
  action: string;
  description?: string;
}

export interface Rol {
  id: number;
  nombre: string;
  descripcion: string;
  permisos: string[];
  activo: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  usuario: Usuario;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  rolId: number;
}
