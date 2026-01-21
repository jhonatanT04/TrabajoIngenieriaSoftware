import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface DashboardMetrics {
  ventas_hoy: number;
  total_productos: number;
  total_usuarios: number;
  total_proveedores: number;
  total_clientes: number;
  stock_bajo: number;
}

export interface RecentActivity {
  title: string;
  description: string;
  time: string;
  type: string;
  timestamp: string;
}

export interface SalesSummary {
  period_days: number;
  total_sales: number;
  count_sales: number;
  average_sale: number;
  start_date: string;
  end_date: string;
}

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private baseUrl = `${environment.apiUrl}/dashboard`;

  constructor(private http: HttpClient) {}

  getMetrics(): Observable<DashboardMetrics> {
    return this.http.get<DashboardMetrics>(`${this.baseUrl}/metrics`);
  }

  getRecentActivity(limit: number = 10): Observable<RecentActivity[]> {
    return this.http.get<RecentActivity[]>(`${this.baseUrl}/recent-activity`, {
      params: { limit: limit.toString() }
    });
  }

  getSalesSummary(days: number = 7): Observable<SalesSummary> {
    return this.http.get<SalesSummary>(`${this.baseUrl}/sales-summary`, {
      params: { days: days.toString() }
    });
  }
}
