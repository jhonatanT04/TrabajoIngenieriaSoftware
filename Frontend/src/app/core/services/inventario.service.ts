import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface InventoryItem {
  id: string;
  product_id: string;
  location_id?: string;
  quantity: number;
  last_updated: string;
  updated_by?: string;
}

export interface InventoryMovement {
  id: string;
  product_id: string;
  movement_type: string;
  quantity: number;
  previous_stock: number;
  new_stock: number;
  reason?: string;
  reference_document?: string;
  user_id: string;
  created_at: string;
}

export interface InventoryAdjustmentRequest {
  product_id: string;
  new_quantity: number;
  reason: string;
}

@Injectable({ providedIn: 'root' })
export class InventarioService {
  private apiUrl = `${environment.apiUrl}/inventory`;

  constructor(private http: HttpClient) {}

  getAll(params?: any): Observable<InventoryItem[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<InventoryItem[]>(this.apiUrl, { params: httpParams });
  }

  getByProduct(productId: string): Observable<InventoryItem> {
    return this.http.get<InventoryItem>(`${this.apiUrl}/${productId}`);
  }

  adjustInventory(data: InventoryAdjustmentRequest): Observable<InventoryItem> {
    return this.http.post<InventoryItem>(`${this.apiUrl}/adjustment`, data);
  }

  getMovements(params?: any): Observable<InventoryMovement[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<InventoryMovement[]>(`${this.apiUrl}/movements`, { params: httpParams });
  }

  getProductMovements(productId: string, params?: any): Observable<InventoryMovement[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<InventoryMovement[]>(`${this.apiUrl}/movements/${productId}`, { params: httpParams });
  }

  getLowStock(): Observable<InventoryItem[]> {
    return this.http.get<InventoryItem[]>(this.apiUrl, { params: { low_stock: 'true' } });
  }
}

