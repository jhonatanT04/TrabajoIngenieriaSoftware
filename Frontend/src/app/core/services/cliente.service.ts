import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Cliente } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ClienteService {
  private apiUrl = `${environment.apiUrl}/customers`;

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

  getById(id: string): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/${id}`);
  }

  getByDocumento(documento: string): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/document/${documento}`);
  }

  create(data: Partial<Cliente>): Observable<Cliente> {
    return this.http.post<Cliente>(this.apiUrl, data);
  }

  update(id: string, data: Partial<Cliente>): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.apiUrl}/${id}`, data);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  search(query: string): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${this.apiUrl}/search/name`, {
      params: { name: query }
    });
  }

  getPuntosFidelidad(clienteId: string): Observable<number> {
    return this.getById(clienteId).pipe(map(c => (c as any)?.loyalty_points ?? 0));
  }

  canjearPuntos(clienteId: string, puntos: number): Observable<any> {
    // Backend suma puntos: usar negativos para canje
    return this.http.post(`${this.apiUrl}/${clienteId}/loyalty-points`, { points: -Math.abs(puntos) });
  }

  agregarPuntos(clienteId: string, puntos: number): Observable<Cliente> {
    return this.http.post<Cliente>(`${this.apiUrl}/${clienteId}/loyalty-points`, { points: Math.abs(puntos) });
  }
}
