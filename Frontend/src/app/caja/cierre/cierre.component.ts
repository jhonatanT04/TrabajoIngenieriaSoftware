import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RouterModule, Router, ActivatedRoute } from '@angular/router';
import { CajaService, CashSession, CashTransaction, CashRegister } from '../services/caja.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  standalone: true,
  selector: 'app-cierre',
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule],
  templateUrl: './cierre.component.html',
  styleUrls: ['./cierre.component.css']
})
export class CierreComponent implements OnInit, OnDestroy {
  currentSession: CashSession | null = null;
  cashRegister: CashRegister | null = null;
  transactions: CashTransaction[] = [];
  cierreForm: FormGroup;
  loading = false;
  errorMessage = '';
  successMessage = '';
  get isClosed(): boolean {
    return (this.currentSession?.status || '').toLowerCase() === 'cerrada';
  }

  private destroy$ = new Subject<void>();

  constructor(
    private cajaService: CajaService,
    public router: Router,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder
  ) {
    this.cierreForm = this.formBuilder.group({
      actual_closing_amount: ['', [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {
    this.route.queryParams.pipe(takeUntil(this.destroy$)).subscribe(params => {
      if (params['session_id']) {
        this.loadSession(params['session_id']);
      } else {
        this.loadActiveSession();
      }
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadCashRegister(cashRegisterId: string): void {
    this.cajaService.getCashRegisters(true)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          const registers = response.data || [];
          this.cashRegister = registers.find((r: CashRegister) => r.id === cashRegisterId) || null;
        },
        error: (error) => {
          console.error('Error al cargar caja:', error);
        }
      });
  }

  loadActiveSession(): void {
    this.loading = true;
    this.cajaService.getActiveSession()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (session) => {
          if (session) {
            this.currentSession = session;
            this.loadCashRegister(session.cash_register_id);
            this.loadTransactions(session.id);
          } else {
            this.errorMessage = 'No hay sesión de caja abierta';
            this.loading = false;
          }
        },
        error: (error) => {
          this.errorMessage = 'Error al cargar sesión: ' + (error.error?.detail || error.message);
          this.loading = false;
        }
      });
  }

  loadSession(sessionId: string): void {
    this.loading = true;
    this.cajaService.getSession(sessionId)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (session) => {
          this.currentSession = session;
          this.loadCashRegister(session.cash_register_id);
          this.loadTransactions(session.id);
        },
        error: (error) => {
          this.errorMessage = 'Error al cargar sesión: ' + (error.error?.detail || error.message);
          this.loading = false;
        }
      });
  }

  loadTransactions(sessionId: string): void {
    this.cajaService.listTransactions(sessionId)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (transactions) => {
          this.transactions = transactions;
          this.loading = false;
        },
        error: (error) => {
          this.errorMessage = 'Error al cargar transacciones: ' + (error.error?.detail || error.message);
          this.loading = false;
        }
      });
  }

  onClose(): void {
    if (!this.currentSession) return;
    
    if (!this.cierreForm.valid) {
      this.errorMessage = 'Por favor ingresa un monto válido';
      return;
    }

    if (!confirm(`¿Está seguro que desea cerrar la caja? La diferencia será: S/ ${this.difference.toFixed(2)}`)) {
      return;
    }

    this.loading = true;
    const closeData = {
      actual_closing_amount: parseFloat(this.cierreForm.get('actual_closing_amount')?.value || '0'),
      notes: ''
    };

    this.cajaService.closeSession(this.currentSession.id, closeData)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (session) => {
          this.successMessage = 'Caja cerrada exitosamente';
          this.currentSession = session;
          this.loading = false;
          setTimeout(() => {
            this.router.navigate(['/caja/apertura']);
          }, 1500);
        },
        error: (error) => {
          this.errorMessage = 'Error al cerrar caja: ' + (error.error?.detail || error.message);
          this.loading = false;
        }
      });
  }

  get totalCashIn(): number {
    if (!this.transactions) return 0;
    return this.transactions
      .filter(t => t.transaction_type === 'ingreso' || t.transaction_type === 'venta')
      .reduce((sum, t) => sum + t.amount, 0);
  }

  get totalCashOut(): number {
    if (!this.transactions) return 0;
    return this.transactions
      .filter(t => t.transaction_type === 'egreso')
      .reduce((sum, t) => sum + t.amount, 0);
  }

  get expectedAmount(): number {
    if (!this.currentSession) return 0;
    return this.currentSession.opening_amount + this.totalCashIn - this.totalCashOut;
  }

  get actualAmount(): number {
    return parseFloat(this.cierreForm.get('actual_closing_amount')?.value || '0');
  }

  get difference(): number {
    return this.actualAmount - this.expectedAmount;
  }

  clearMessages(): void {
    this.errorMessage = '';
    this.successMessage = '';
  }

  hasClosingAmountError(): boolean {
    return (this.cierreForm.get('actual_closing_amount')?.invalid && 
           this.cierreForm.get('actual_closing_amount')?.touched) || false;
  }
}
