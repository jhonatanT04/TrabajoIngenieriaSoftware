import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Proveedor, OrdenCompra, OrdenCompraCreateRequest } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ProveedorService {
  private apiUrl = `${environment.apiUrl}/proveedores`;

  constructor(private http: HttpClient) {}

  
  getAll(): Observable<Proveedor[]> {
    return this.http.get<Proveedor[]>(this.apiUrl);
  }

  
  getById(id: number): Observable<Proveedor> {
    return this.http.get<Proveedor>(`${this.apiUrl}/${id}`);
  }

  
  create(data: Partial<Proveedor>): Observable<Proveedor> {
    return this.http.post<Proveedor>(this.apiUrl, data);
  }

  
  update(id: number, data: Partial<Proveedor>): Observable<Proveedor> {
    return this.http.put<Proveedor>(`${this.apiUrl}/${id}`, data);
  }

  
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  
  search(query: string): Observable<Proveedor[]> {
    return this.http.get<Proveedor[]>(`${this.apiUrl}/search`, {
      params: { q: query }
    });
  }


  
  getOrdenes(): Observable<OrdenCompra[]> {
    return this.http.get<OrdenCompra[]>(`${environment.apiUrl}/ordenes-compra`);
  }

  
  getOrdenById(id: number): Observable<OrdenCompra> {
    return this.http.get<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}`);
  }

  
  createOrden(data: OrdenCompraCreateRequest): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra`, data);
  }

  
  updateOrden(id: number, data: Partial<OrdenCompra>): Observable<OrdenCompra> {
    return this.http.put<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}`, data);
  }

  
  cancelOrden(id: number, motivo: string): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}/cancelar`, { motivo });
  }

  
  aprobarOrden(id: number): Observable<OrdenCompra> {
    return this.http.post<OrdenCompra>(`${environment.apiUrl}/ordenes-compra/${id}/aprobar`, {});
  }
}
