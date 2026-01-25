import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface FiltroReporte {
  fecha_inicio?: string;
  fecha_fin?: string;
  categoria_id?: string;
  producto_id?: string;
  cliente_id?: string;
  usuario_id?: string;
}

@Injectable({ providedIn: 'root' })
export class ReportesService {
  private apiUrl = `${environment.apiUrl}`;

  constructor(private http: HttpClient) {}

  reporteVentas(filtro?: FiltroReporte): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/sales`);
  }

  reporteInventario(filtro?: FiltroReporte): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/inventory/movement-list`);
  }

  reporteCaja(filtro?: FiltroReporte): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/caja/cash-sessions`);
  }

  reporteClientes(filtro?: FiltroReporte): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/customers`);
  }

  exportarExcel(tipo: string, filtro?: FiltroReporte): Observable<Blob> {
    return this.http.post(
      `${this.apiUrl}/reportes/exportar/excel`,
      { tipo, filtro: filtro || {} },
      { responseType: 'blob' }
    );
  }

  exportarCSV(tipo: string, filtro?: FiltroReporte): Observable<Blob> {
    return this.http.post(
      `${this.apiUrl}/reportes/exportar/csv`,
      { tipo, filtro: filtro || {} },
      { responseType: 'blob' }
    );
  }

  exportarPDF(tipo: string, filtro?: FiltroReporte): Observable<Blob> {
    return this.http.post(
      `${this.apiUrl}/reportes/exportar/pdf`,
      { tipo, filtro: filtro || {} },
      { responseType: 'blob' }
    );
  }

  descargarArchivo(blob: Blob, nombre: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = nombre;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
}
