import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface CashSession {
  id: string;
  cash_register_id: string;
  user_id: string;
  user?: {
    id: string;
    username: string;
    first_name: string;
    last_name: string;
  };
  opening_date: string;
  closing_date?: string;
  opening_amount: number;
  expected_closing_amount: number;
  actual_closing_amount: number;
  difference: number;
  status: string;
  notes?: string;
}

export interface CashTransaction {
  id: string;
  session_id: string;
  transaction_type: string;
  amount: number;
  payment_method_id: string;
  reference_number?: string;
  description?: string;
  created_at: string;
  created_by: string;
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

export interface TransactionCreateRequest {
  transaction_type: string;
  amount: number;
  payment_method_id: string;
  reference_number?: string;
  description?: string;
}

export interface CashRegister {
  id: string;
  register_number: string;
  location?: string;
  is_active: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class CajaService {
  private apiUrl = `${environment.apiUrl}/caja`;
  private activeSessionSubject = new BehaviorSubject<CashSession | null>(null);
  public activeSession$ = this.activeSessionSubject.asObservable();

  constructor(private http: HttpClient) {}

  getCashRegisters(isActive: boolean = true): Observable<any> {
    return this.http.get(`${this.apiUrl}/cash-registers?is_active=${isActive}`);
  }

  getActiveSession(): Observable<CashSession | null> {
    return this.http.get<CashSession | null>(`${this.apiUrl}/cash-sessions/user/active`);
  }

  updateActiveSession(): void {
    this.getActiveSession().subscribe(session => {
      this.activeSessionSubject.next(session);
    });
  }

  getCurrentActiveSession(): CashSession | null {
    return this.activeSessionSubject.value;
  }

  openSession(data: SessionOpenRequest): Observable<CashSession> {
    return this.http.post<CashSession>(`${this.apiUrl}/cash-sessions/open`, data);
  }

  closeSession(sessionId: string, data: SessionCloseRequest): Observable<CashSession> {
    return this.http.post<CashSession>(`${this.apiUrl}/cash-sessions/${sessionId}/close`, data);
  }

  listSessions(skip: number = 0, limit: number = 100, status?: string): Observable<CashSession[]> {
    let url = `${this.apiUrl}/cash-sessions?skip=${skip}&limit=${limit}`;
    if (status) {
      url += `&status=${status}`;
    }
    return this.http.get<CashSession[]>(url);
  }

  getSession(sessionId: string): Observable<CashSession> {
    return this.http.get<CashSession>(`${this.apiUrl}/cash-sessions/${sessionId}`);
  }

  createTransaction(sessionId: string, transaction: TransactionCreateRequest): Observable<CashTransaction> {
    return this.http.post<CashTransaction>(
      `${this.apiUrl}/cash-sessions/${sessionId}/transactions`,
      transaction
    );
  }

  listTransactions(sessionId: string): Observable<CashTransaction[]> {
    return this.http.get<CashTransaction[]>(`${this.apiUrl}/cash-sessions/${sessionId}/transactions`);
  }

  getSummary(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/cash-sessions/status/summary`);
  }
}
