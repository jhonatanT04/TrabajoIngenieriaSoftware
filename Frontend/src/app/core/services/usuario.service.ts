import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Usuario, Rol } from '../models';
import { environment } from '../../../environments/environment';

/**
 * Servicio de Usuarios
 * Gestiona usuarios y roles del sistema
 */
@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  private apiUrl = `${environment.apiUrl}/usuarios`;

  constructor(private http: HttpClient) {}

  /**
   * Obtener todos los usuarios
   */
  getAll(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.apiUrl);
  }

  /**
   * Obtener usuario por ID
   */
  getById(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.apiUrl}/${id}`);
  }

  /**
   * Crear nuevo usuario
   */
  create(data: Partial<Usuario>): Observable<Usuario> {
    return this.http.post<Usuario>(this.apiUrl, data);
  }

  /**
   * Actualizar usuario
   */
  update(id: number, data: Partial<Usuario>): Observable<Usuario> {
    return this.http.put<Usuario>(`${this.apiUrl}/${id}`, data);
  }

  /**
   * Eliminar usuario
   */
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  /**
   * Cambiar contraseña
   */
  changePassword(id: number, oldPassword: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/cambiar-password`, {
      oldPassword,
      newPassword
    });
  }

  /**
   * Activar/Desactivar usuario
   */
  toggleActive(id: number, activo: boolean): Observable<Usuario> {
    return this.http.patch<Usuario>(`${this.apiUrl}/${id}/toggle-active`, { activo });
  }

  // Roles

  /**
   * Obtener todos los roles
   */
  getRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(`${environment.apiUrl}/roles`);
  }

  /**
   * Obtener rol por ID
   */
  getRolById(id: number): Observable<Rol> {
    return this.http.get<Rol>(`${environment.apiUrl}/roles/${id}`);
  }

  /**
   * Crear rol
   */
  createRol(data: Partial<Rol>): Observable<Rol> {
    return this.http.post<Rol>(`${environment.apiUrl}/roles`, data);
  }

  /**
   * Actualizar rol
   */
  updateRol(id: number, data: Partial<Rol>): Observable<Rol> {
    return this.http.put<Rol>(`${environment.apiUrl}/roles/${id}`, data);
  }

  /**
   * Eliminar rol
   */
  deleteRol(id: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/roles/${id}`);
  }
}
