import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Venta, VentaItem, Cliente, Promocion } from '../models';
import { environment } from '../../../environments/environment';

/**
 * Servicio de Ventas
 * Gestiona las operaciones de ventas, clientes y promociones
 */
@Injectable({
  providedIn: 'root'
})
export class VentaService {
  private apiUrl = `${environment.apiUrl}/ventas`;

  constructor(private http: HttpClient) {}

  /**
   * Obtener todas las ventas
   */
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

  /**
   * Obtener venta por ID
   */
  getById(id: number): Observable<Venta> {
    return this.http.get<Venta>(`${this.apiUrl}/${id}`);
  }

  /**
   * Crear nueva venta
   */
  create(data: Partial<Venta>): Observable<Venta> {
    return this.http.post<Venta>(this.apiUrl, data);
  }

  /**
   * Cancelar venta
   */
  cancel(id: number, motivo: string): Observable<Venta> {
    return this.http.post<Venta>(`${this.apiUrl}/${id}/cancelar`, { motivo });
  }

  /**
   * Obtener ventas por fecha
   */
  getByFecha(fechaInicio: Date, fechaFin: Date): Observable<Venta[]> {
    return this.http.get<Venta[]>(`${this.apiUrl}/por-fecha`, {
      params: {
        fechaInicio: fechaInicio.toISOString(),
        fechaFin: fechaFin.toISOString()
      }
    });
  }

  /**
   * Obtener ventas por cliente
   */
  getByCliente(clienteId: number): Observable<Venta[]> {
    return this.http.get<Venta[]>(`${this.apiUrl}/cliente/${clienteId}`);
  }
}
