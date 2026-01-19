import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Usuario, Rol } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  private apiUrl = `${environment.apiUrl}/users`;
  private authUrl = `${environment.apiUrl}/auth`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.apiUrl);
  }

  getById(id: string): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.apiUrl}/${id}`);
  }

  create(data: Partial<Usuario>): Observable<Usuario> {
    return this.http.post<Usuario>(this.apiUrl, data);
  }

  update(id: string, data: Partial<Usuario>): Observable<Usuario> {
    return this.http.put<Usuario>(`${this.apiUrl}/${id}`, data);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  // El backend cambia contraseña del usuario actual, no por ID
  changePassword(currentPassword: string, newPassword: string): Observable<any> {
    return this.http.put(`${this.authUrl}/change-password`, {
      current_password: currentPassword,
      new_password: newPassword
    });
  }

  // Activar/desactivar según boolean
  toggleActive(id: string, activo: boolean): Observable<Usuario> {
    if (activo) {
      return this.http.put<Usuario>(`${this.apiUrl}/${id}/activate`, {});
    }
    return this.http.delete<Usuario>(`${this.apiUrl}/${id}/deactivate`);
  }

  // Gestión de roles (perfiles) no está expuesta en backend por ahora
  getRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(`${environment.apiUrl}/roles`);
  }

  getRolById(id: string): Observable<Rol> {
    return this.http.get<Rol>(`${environment.apiUrl}/roles/${id}`);
  }

  createRol(data: Partial<Rol>): Observable<Rol> {
    return this.http.post<Rol>(`${environment.apiUrl}/roles`, data);
  }

  updateRol(id: string, data: Partial<Rol>): Observable<Rol> {
    return this.http.put<Rol>(`${environment.apiUrl}/roles/${id}`, data);
  }

  deleteRol(id: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/roles/${id}`);
  }
}
