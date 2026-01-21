import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Venta, VentaItem, Cliente, Promocion } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class VentaService {
  private apiUrl = `${environment.apiUrl}/sales`;

  constructor(private http: HttpClient) {}

  
  getAll(params?: any): Observable<Venta[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<Venta[]>(this.apiUrl, { params: httpParams });
  }

  
  getById(id: string | number): Observable<Venta> {
    return this.http.get<Venta>(`${this.apiUrl}/${id}`);
  }

  
  create(data: Partial<Venta>): Observable<Venta> {
    return this.http.post<Venta>(this.apiUrl, data);
  }

  
  delete(id: string | number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  
  cancel(id: number, motivo: string): Observable<Venta> {
    return this.http.post<Venta>(`${this.apiUrl}/${id}/cancelar`, { motivo });
  }

  
  getByFecha(fechaInicio: Date, fechaFin: Date): Observable<Venta[]> {
    return this.http.get<Venta[]>(`${this.apiUrl}/por-fecha`, {
      params: {
        fechaInicio: fechaInicio.toISOString(),
        fechaFin: fechaFin.toISOString()
      }
    });
  }

  
  getByCliente(clienteId: number): Observable<Venta[]> {
    return this.http.get<Venta[]>(`${this.apiUrl}/cliente/${clienteId}`);
  }
}
