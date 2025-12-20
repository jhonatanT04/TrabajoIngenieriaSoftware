import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  ReporteVentas,
  ReporteInventario,
  ReporteCaja,
  ReporteClientes,
  FiltroReporte
} from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ReporteService {
  private apiUrl = `${environment.apiUrl}/reportes`;

  constructor(private http: HttpClient) {}

  
  getReporteVentas(filtro: FiltroReporte): Observable<ReporteVentas> {
    return this.http.post<ReporteVentas>(`${this.apiUrl}/ventas`, filtro);
  }

  
  getReporteInventario(filtro?: FiltroReporte): Observable<ReporteInventario> {
    return this.http.post<ReporteInventario>(`${this.apiUrl}/inventario`, filtro || {});
  }

  
  getReporteCaja(filtro: FiltroReporte): Observable<ReporteCaja> {
    return this.http.post<ReporteCaja>(`${this.apiUrl}/caja`, filtro);
  }

  
  getReporteClientes(filtro?: FiltroReporte): Observable<ReporteClientes> {
    return this.http.post<ReporteClientes>(`${this.apiUrl}/clientes`, filtro || {});
  }

  
  exportarExcel(tipo: string, filtro: FiltroReporte): Observable<Blob> {
    return this.http.post(`${this.apiUrl}/exportar/excel`,
      { tipo, filtro },
      { responseType: 'blob' }
    );
  }

  
  exportarCSV(tipo: string, filtro: FiltroReporte): Observable<Blob> {
    return this.http.post(`${this.apiUrl}/exportar/csv`,
      { tipo, filtro },
      { responseType: 'blob' }
    );
  }

  
  exportarPDF(tipo: string, filtro: FiltroReporte): Observable<Blob> {
    return this.http.post(`${this.apiUrl}/exportar/pdf`,
      { tipo, filtro },
      { responseType: 'blob' }
    );
  }
}
