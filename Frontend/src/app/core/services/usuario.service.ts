import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Usuario, Rol } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  private apiUrl = `${environment.apiUrl}/usuarios`;

  constructor(private http: HttpClient) {}

  
  getAll(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.apiUrl);
  }

  
  getById(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.apiUrl}/${id}`);
  }

  
  create(data: Partial<Usuario>): Observable<Usuario> {
    return this.http.post<Usuario>(this.apiUrl, data);
  }

  
  update(id: number, data: Partial<Usuario>): Observable<Usuario> {
    return this.http.put<Usuario>(`${this.apiUrl}/${id}`, data);
  }

  
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  
  changePassword(id: number, oldPassword: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/cambiar-password`, {
      oldPassword,
      newPassword
    });
  }

  
  toggleActive(id: number, activo: boolean): Observable<Usuario> {
    return this.http.patch<Usuario>(`${this.apiUrl}/${id}/toggle-active`, { activo });
  }


  
  getRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(`${environment.apiUrl}/roles`);
  }

  
  getRolById(id: number): Observable<Rol> {
    return this.http.get<Rol>(`${environment.apiUrl}/roles/${id}`);
  }

  
  createRol(data: Partial<Rol>): Observable<Rol> {
    return this.http.post<Rol>(`${environment.apiUrl}/roles`, data);
  }

  
  updateRol(id: number, data: Partial<Rol>): Observable<Rol> {
    return this.http.put<Rol>(`${environment.apiUrl}/roles/${id}`, data);
  }

  
  deleteRol(id: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/roles/${id}`);
  }
}
