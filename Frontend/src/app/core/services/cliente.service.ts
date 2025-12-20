import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cliente } from '../models';
import { environment } from '../../../environments/environment';

/**
 * Servicio de Clientes
 * Gestiona las operaciones CRUD de clientes y programa de fidelidad
 */
@Injectable({
  providedIn: 'root'
})
export class ClienteService {
  private apiUrl = `${environment.apiUrl}/clientes`;

  constructor(private http: HttpClient) {}

  /**
   * Obtener todos los clientes
   */
  getAll(params?: any): Observable<Cliente[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<Cliente[]>(this.apiUrl, { params: httpParams });
  }

  /**
   * Obtener cliente por ID
   */
  getById(id: number): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/${id}`);
  }

  /**
   * Buscar cliente por documento
   */
  getByDocumento(documento: string): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/documento/${documento}`);
  }

  /**
   * Crear nuevo cliente
   */
  create(data: Partial<Cliente>): Observable<Cliente> {
    return this.http.post<Cliente>(this.apiUrl, data);
  }

  /**
   * Actualizar cliente
   */
  update(id: number, data: Partial<Cliente>): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.apiUrl}/${id}`, data);
  }

  /**
   * Eliminar cliente
   */
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  /**
   * Buscar clientes
   */
  search(query: string): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${this.apiUrl}/search`, {
      params: { q: query }
    });
  }

  /**
   * Obtener puntos de fidelidad
   */
  getPuntosFidelidad(clienteId: number): Observable<number> {
    return this.http.get<number>(`${this.apiUrl}/${clienteId}/puntos`);
  }

  /**
   * Canjear puntos
   */
  canjearPuntos(clienteId: number, puntos: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${clienteId}/canjear`, { puntos });
  }

  /**
   * Agregar puntos
   */
  agregarPuntos(clienteId: number, puntos: number): Observable<Cliente> {
    return this.http.post<Cliente>(`${this.apiUrl}/${clienteId}/agregar-puntos`, { puntos });
  }
}
