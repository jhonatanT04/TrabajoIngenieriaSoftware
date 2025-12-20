import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Parametro, ConfiguracionGeneral } from '../models';
import { environment } from '../../../environments/environment';

/**
 * Servicio de Parámetros
 * Gestiona configuraciones del sistema
 */
@Injectable({
  providedIn: 'root'
})
export class ParametroService {
  private apiUrl = `${environment.apiUrl}/parametros`;

  constructor(private http: HttpClient) {}

  /**
   * Obtener todos los parámetros
   */
  getAll(): Observable<Parametro[]> {
    return this.http.get<Parametro[]>(this.apiUrl);
  }

  /**
   * Obtener parámetro por código
   */
  getByCodigo(codigo: string): Observable<Parametro> {
    return this.http.get<Parametro>(`${this.apiUrl}/codigo/${codigo}`);
  }

  /**
   * Obtener parámetros por grupo
   */
  getByGrupo(grupo: string): Observable<Parametro[]> {
    return this.http.get<Parametro[]>(`${this.apiUrl}/grupo/${grupo}`);
  }

  /**
   * Actualizar parámetro
   */
  update(id: number, valor: string): Observable<Parametro> {
    return this.http.put<Parametro>(`${this.apiUrl}/${id}`, { valor });
  }

  /**
   * Obtener configuración general
   */
  getConfiguracionGeneral(): Observable<ConfiguracionGeneral> {
    return this.http.get<ConfiguracionGeneral>(`${this.apiUrl}/configuracion-general`);
  }

  /**
   * Actualizar configuración general
   */
  updateConfiguracionGeneral(data: Partial<ConfiguracionGeneral>): Observable<ConfiguracionGeneral> {
    return this.http.put<ConfiguracionGeneral>(`${this.apiUrl}/configuracion-general`, data);
  }
}
