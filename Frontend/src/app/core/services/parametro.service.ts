import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Parametro, ConfiguracionGeneral } from '../models';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ParametroService {
  private apiUrl = `${environment.apiUrl}/parametros`;

  constructor(private http: HttpClient) {}

  
  getAll(): Observable<Parametro[]> {
    return this.http.get<Parametro[]>(this.apiUrl);
  }

  
  getByCodigo(codigo: string): Observable<Parametro> {
    return this.http.get<Parametro>(`${this.apiUrl}/codigo/${codigo}`);
  }

  
  getByGrupo(grupo: string): Observable<Parametro[]> {
    return this.http.get<Parametro[]>(`${this.apiUrl}/grupo/${grupo}`);
  }

  
  update(id: number, valor: string): Observable<Parametro> {
    return this.http.put<Parametro>(`${this.apiUrl}/${id}`, { valor });
  }

  
  getConfiguracionGeneral(): Observable<ConfiguracionGeneral> {
    return this.http.get<ConfiguracionGeneral>(`${this.apiUrl}/configuracion-general`);
  }

  
  updateConfiguracionGeneral(data: Partial<ConfiguracionGeneral>): Observable<ConfiguracionGeneral> {
    return this.http.put<ConfiguracionGeneral>(`${this.apiUrl}/configuracion-general`, data);
  }
}
