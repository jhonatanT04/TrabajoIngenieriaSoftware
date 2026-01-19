import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Proveedor, OrdenCompra, OrdenCompraCreateRequest } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ProveedorService {
  private apiUrl = `${environment.apiUrl}/suppliers`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Proveedor[]> {
    return this.http.get<Proveedor[]>(this.apiUrl);
  }

  // Nota: El backend actual no expone GET/PUT/DELETE por id para proveedores.
  // Estas funciones pueden fallar hasta implementar dichos endpoints.
  getById(id: string): Observable<Proveedor> {
    return this.http.get<Proveedor>(`${this.apiUrl}/${id}`);
  }

  create(data: Partial<Proveedor>): Observable<Proveedor> {
    return this.http.post<Proveedor>(this.apiUrl, data);
  }

  update(id: string, data: Partial<Proveedor>): Observable<Proveedor> {
    return this.http.put<Proveedor>(`${this.apiUrl}/${id}`, data);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  // Búsqueda no implementada en backend; se mantiene firma por compatibilidad
  search(query: string): Observable<Proveedor[]> {
    return this.http.get<Proveedor[]>(`${this.apiUrl}`, { params: { q: query } });
  }

  // Módulo de órdenes de compra no existe en rutas del backend aún
  getOrdenes(): Observable<OrdenCompra[]> {
    return this.http.get<OrdenCompra[]>(`${environment.apiUrl}/ordenes-compra`);
  }

  getOrdenById(id: string): Observable<OrdenCompra> {
    return this.http.get<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}`);
  }

  createOrden(data: OrdenCompraCreateRequest): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra`, data);
  }

  updateOrden(id: string, data: Partial<OrdenCompra>): Observable<OrdenCompra> {
    return this.http.put<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}`, data);
  }

  cancelOrden(id: string, motivo: string): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}/cancelar`, { motivo });
  }

  aprobarOrden(id: string): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}/aprobar`, {});
  }
}
