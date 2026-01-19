import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface CashSession {
  id: string;
  cash_register_id: string;
  user_id: string;
  opening_date: string;
  closing_date?: string;
  opening_amount: number;
  expected_closing_amount: number;
  actual_closing_amount: number;
  difference: number;
  status: string;
  notes?: string;
}

export interface SessionOpenRequest {
  cash_register_id: string;
  opening_amount: number;
  notes?: string;
}

export interface SessionCloseRequest {
  actual_closing_amount: number;
  notes?: string;
}

export interface CashTransaction {
  id?: string;
  session_id?: string;
  transaction_type: string;
  amount: number;
  payment_method_id: string;
  reference_number?: string;
  description?: string;
  created_at?: string;
  created_by?: string;
}

@Injectable({
  providedIn: 'root'
})
export class CajaService {
  private apiUrl = `${environment.apiUrl}/cash-sessions`;

  constructor(private http: HttpClient) {}

  openSession(data: SessionOpenRequest): Observable<CashSession> {
    return this.http.post<CashSession>(`${this.apiUrl}/open`, data);
  }

  closeSession(sessionId: string, data: SessionCloseRequest): Observable<CashSession> {
    return this.http.post<CashSession>(`${this.apiUrl}/${sessionId}/close`, data);
  }

  getSessions(params?: any): Observable<CashSession[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<CashSession[]>(this.apiUrl, { params: httpParams });
  }

  getSession(sessionId: string): Observable<CashSession> {
    return this.http.get<CashSession>(`${this.apiUrl}/${sessionId}`);
  }

  createTransaction(sessionId: string, data: CashTransaction): Observable<CashTransaction> {
    return this.http.post<CashTransaction>(`${this.apiUrl}/${sessionId}/transactions`, data);
  }

  getSessionTransactions(sessionId: string): Observable<CashTransaction[]> {
    return this.http.get<CashTransaction[]>(`${this.apiUrl}/${sessionId}/transactions`);
  }
}
