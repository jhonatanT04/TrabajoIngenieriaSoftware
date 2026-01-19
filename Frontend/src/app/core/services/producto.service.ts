import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Producto, Categoria, ProductoCreateRequest } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ProductoService {
  private apiUrl = `${environment.apiUrl}/products`;

  constructor(private http: HttpClient) {}

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

  getById(id: string): Observable<Producto> {
    return this.http.get<Producto>(`${this.apiUrl}/${id}`);
  }

  getByCodigo(codigo: string): Observable<Producto> {
    return this.http.get<Producto>(`${this.apiUrl}/sku/${codigo}`);
  }

  create(data: ProductoCreateRequest): Observable<Producto> {
    return this.http.post<Producto>(this.apiUrl, data);
  }

  update(id: string, data: Partial<Producto>): Observable<Producto> {
    return this.http.put<Producto>(`${this.apiUrl}/${id}`, data);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  search(query: string): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.apiUrl}/search/name`, {
      params: { name: query }
    });
  }

  getStockBajo(): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.apiUrl}/low-stock/list`);
  }

  getCategorias(): Observable<Categoria[]> {
    return this.http.get<Categoria[]>(`${environment.apiUrl}/categories`);
  }

  createCategoria(data: Partial<Categoria>): Observable<Categoria> {
    return this.http.post<Categoria>(`${environment.apiUrl}/categories`, data);
  }

  updateCategoria(id: string, data: Partial<Categoria>): Observable<Categoria> {
    return this.http.put<Categoria>(`${environment.apiUrl}/categories/${id}`, data);
  }

  deleteCategoria(id: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/categories/${id}`);
  }
}
