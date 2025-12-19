import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { delay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // Usuario actual en memoria
  private currentUserSubject = new BehaviorSubject<any>(null);
  currentUser$ = this.currentUserSubject.asObservable();

  constructor() {
    // Restaurar sesión si existe
    const user = localStorage.getItem('user');
    if (user) {
      this.currentUserSubject.next(JSON.parse(user));
    }
  }

  login(username: string, password: string): Observable<any> {

    if (username === 'admin' && password === 'admin') {
      return this.setSession({
        username,
        role: 'ADMIN',
        token: 'jwt-mock'
      });
    }

    if (username === 'cajero' && password === '1234') {
      return this.setSession({
        username,
        role: 'CAJERO',
        token: 'jwt-mock'
      });
    }

    return throwError(() => new Error('Credenciales inválidas'));
  }

  register(data: any): Observable<any> {
    // Mock de registro
    return of({ success: true }).pipe(delay(1000));
  }

  forgotPassword(email: string): Observable<any> {
    // Mock de recuperación
    return of({ message: 'Correo enviado' }).pipe(delay(1000));
  }

  /* =========================
     SESIÓN
  ========================== */

  private setSession(user: any): Observable<any> {
    localStorage.setItem('user', JSON.stringify(user));
    this.currentUserSubject.next(user);
    return of(user).pipe(delay(800));
  }

  logout(): void {
    localStorage.removeItem('user');
    this.currentUserSubject.next(null);
  }

  /* =========================
     HELPERS PARA GUARDS
  ========================== */

  isAuthenticated(): boolean {
    return !!localStorage.getItem('user');
  }

  getUser(): any {
    return this.currentUserSubject.value;
  }

  getRole(): string | null {
    return this.getUser()?.role || null;
  }
}
