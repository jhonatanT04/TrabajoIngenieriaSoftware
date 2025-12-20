import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Proveedor, OrdenCompra, OrdenCompraCreateRequest } from '../models';
import { environment } from '../../../environments/environment';

/**
 * Servicio de Proveedores
 * Gestiona proveedores y órdenes de compra
 */
@Injectable({
  providedIn: 'root'
})
export class ProveedorService {
  private apiUrl = `${environment.apiUrl}/proveedores`;

  constructor(private http: HttpClient) {}

  /**
   * Obtener todos los proveedores
   */
  getAll(): Observable<Proveedor[]> {
    return this.http.get<Proveedor[]>(this.apiUrl);
  }

  /**
   * Obtener proveedor por ID
   */
  getById(id: number): Observable<Proveedor> {
    return this.http.get<Proveedor>(`${this.apiUrl}/${id}`);
  }

  /**
   * Crear nuevo proveedor
   */
  create(data: Partial<Proveedor>): Observable<Proveedor> {
    return this.http.post<Proveedor>(this.apiUrl, data);
  }

  /**
   * Actualizar proveedor
   */
  update(id: number, data: Partial<Proveedor>): Observable<Proveedor> {
    return this.http.put<Proveedor>(`${this.apiUrl}/${id}`, data);
  }

  /**
   * Eliminar proveedor
   */
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  /**
   * Buscar proveedores
   */
  search(query: string): Observable<Proveedor[]> {
    return this.http.get<Proveedor[]>(`${this.apiUrl}/search`, {
      params: { q: query }
    });
  }

  // Órdenes de Compra

  /**
   * Obtener todas las órdenes de compra
   */
  getOrdenes(): Observable<OrdenCompra[]> {
    return this.http.get<OrdenCompra[]>(`${environment.apiUrl}/ordenes-compra`);
  }

  /**
   * Obtener orden de compra por ID
   */
  getOrdenById(id: number): Observable<OrdenCompra> {
    return this.http.get<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}`);
  }

  /**
   * Crear orden de compra
   */
  createOrden(data: OrdenCompraCreateRequest): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra`, data);
  }

  /**
   * Actualizar orden de compra
   */
  updateOrden(id: number, data: Partial<OrdenCompra>): Observable<OrdenCompra> {
    return this.http.put<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}`, data);
  }

  /**
   * Cancelar orden de compra
   */
  cancelOrden(id: number, motivo: string): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}/cancelar`, { motivo });
  }

  /**
   * Aprobar orden de compra
   */
  aprobarOrden(id: number): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}/aprobar`, {});
  }
}
