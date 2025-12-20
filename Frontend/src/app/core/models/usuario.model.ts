/**
 * Modelo de Usuario
 * Representa un usuario del sistema con sus roles y permisos
 */
export interface Usuario {
  id: number;
  username: string;
  email: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  rol: Rol;
  rolId: number;
  activo: boolean;
  fechaCreacion: Date;
  ultimoAcceso?: Date;
  avatar?: string;
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
