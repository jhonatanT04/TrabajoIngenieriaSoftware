import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Producto, Categoria, ProductoCreateRequest } from '../models';
import { environment } from '../../../environments/environment';

/**
 * Servicio de Productos
 * Gestiona las operaciones CRUD de productos y categorías
 */
@Injectable({
  providedIn: 'root'
})
export class ProductoService {
  private apiUrl = `${environment.apiUrl}/productos`;

  constructor(private http: HttpClient) {}

  /**
   * Obtener todos los productos
   */
  getAll(params?: any): Observable<Producto[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<Producto[]>(this.apiUrl, { params: httpParams });
  }

  /**
   * Obtener producto por ID
   */
  getById(id: number): Observable<Producto> {
    return this.http.get<Producto>(`${this.apiUrl}/${id}`);
  }

  /**
   * Obtener producto por código
   */
  getByCodigo(codigo: string): Observable<Producto> {
    return this.http.get<Producto>(`${this.apiUrl}/codigo/${codigo}`);
  }

  /**
   * Crear nuevo producto
   */
  create(data: ProductoCreateRequest): Observable<Producto> {
    return this.http.post<Producto>(this.apiUrl, data);
  }

  /**
   * Actualizar producto
   */
  update(id: number, data: Partial<Producto>): Observable<Producto> {
    return this.http.put<Producto>(`${this.apiUrl}/${id}`, data);
  }

  /**
   * Eliminar producto
   */
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  /**
   * Buscar productos
   */
  search(query: string): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.apiUrl}/search`, {
      params: { q: query }
    });
  }

  /**
   * Obtener productos con stock bajo
   */
  getStockBajo(): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.apiUrl}/stock-bajo`);
  }

  // Categorías

  /**
   * Obtener todas las categorías
   */
  getCategorias(): Observable<Categoria[]> {
    return this.http.get<Categoria[]>(`${environment.apiUrl}/categorias`);
  }

  /**
   * Crear nueva categoría
   */
  createCategoria(data: Partial<Categoria>): Observable<Categoria> {
    return this.http.post<Categoria>(`${environment.apiUrl}/categorias`, data);
  }

  /**
   * Actualizar categoría
   */
  updateCategoria(id: number, data: Partial<Categoria>): Observable<Categoria> {
    return this.http.put<Categoria>(`${environment.apiUrl}/categorias/${id}`, data);
  }

  /**
   * Eliminar categoría
   */
  deleteCategoria(id: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/categorias/${id}`);
  }
}
