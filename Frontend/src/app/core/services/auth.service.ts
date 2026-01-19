import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private currentUserSubject = new BehaviorSubject<any>(null);
  currentUser$ = this.currentUserSubject.asObservable();
  private baseUrl = `${environment.apiUrl}/auth`;

  constructor(private http: HttpClient) {
    const user = localStorage.getItem('user');
    if (user) {
      this.currentUserSubject.next(JSON.parse(user));
    }
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/login`, { username, password }).pipe(
      tap((res) => {
        const sessionUser = {
          id: res?.user?.id,
          username: res?.user?.username,
          email: res?.user?.email,
          first_name: res?.user?.first_name,
          last_name: res?.user?.last_name,
          role: res?.user?.profile_name, // compat: mantener 'role' para guards
          token: res?.access_token,
          tokenType: res?.token_type
        };
        localStorage.setItem('user', JSON.stringify(sessionUser));
        this.currentUserSubject.next(sessionUser);
      })
    );
  }

  register(data: { username: string; email: string; password: string; first_name?: string; last_name?: string; profile_name?: string; }): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/register`, data).pipe(
      tap((res) => {
        const sessionUser = {
          id: res?.user?.id,
          username: res?.user?.username,
          email: res?.user?.email,
          first_name: res?.user?.first_name,
          last_name: res?.user?.last_name,
          role: res?.user?.profile_name,
          token: res?.access_token,
          tokenType: res?.token_type
        };
        localStorage.setItem('user', JSON.stringify(sessionUser));
        this.currentUserSubject.next(sessionUser);
      })
    );
  }

  forgotPassword(email: string): Observable<any> {
    // No endpoint en backend; mantener placeholder
    return of({ message: 'Correo enviado (simulado)' });
  }

  logout(): void {
    localStorage.removeItem('user');
    this.currentUserSubject.next(null);
  }

  isAuthenticated(): boolean {
    const user = localStorage.getItem('user');
    if (!user) return false;
    try {
      const u = JSON.parse(user);
      return !!u?.token;
    } catch {
      return false;
    }
  }

  getUser(): any {
    return this.currentUserSubject.value;
  }

  getRole(): string | null {
    return this.getUser()?.role || null; // 'role' mapeado desde profile_name
  }
}
