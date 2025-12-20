import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cliente } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ClienteService {
  private apiUrl = `${environment.apiUrl}/clientes`;

  constructor(private http: HttpClient) {}

  
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

  
  getById(id: number): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/${id}`);
  }

  
  getByDocumento(documento: string): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/documento/${documento}`);
  }

  
  create(data: Partial<Cliente>): Observable<Cliente> {
    return this.http.post<Cliente>(this.apiUrl, data);
  }

  
  update(id: number, data: Partial<Cliente>): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.apiUrl}/${id}`, data);
  }

  
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  
  search(query: string): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${this.apiUrl}/search`, {
      params: { q: query }
    });
  }

  
  getPuntosFidelidad(clienteId: number): Observable<number> {
    return this.http.get<number>(`${this.apiUrl}/${clienteId}/puntos`);
  }

  
  canjearPuntos(clienteId: number, puntos: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${clienteId}/canjear`, { puntos });
  }

  
  agregarPuntos(clienteId: number, puntos: number): Observable<Cliente> {
    return this.http.post<Cliente>(`${this.apiUrl}/${clienteId}/agregar-puntos`, { puntos });
  }
}
