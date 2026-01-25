import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CajaService, CashSession, CashRegister } from '../services/caja.service';
import { AuthService } from '../../core/services/auth.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  standalone: true,
  selector: 'app-apertura',
  imports: [CommonModule, RouterModule, FormsModule, ReactiveFormsModule],
  templateUrl: './apertura.component.html',
  styleUrls: ['./apertura.component.css']
})
export class AperturaComponent implements OnInit, OnDestroy {
  aperturas: CashSession[] = [];
  activeSession: CashSession | null = null;
  cashRegisters: CashRegister[] = [];
  aperturaForm: FormGroup;
  showForm = false;
  loading = false;
  errorMessage = '';
  successMessage = '';
  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;
  isAdmin = false;
  isCajero = false;
  statusFilter: 'todas' | 'abierta' | 'cerrada' = 'todas';

  private destroy$ = new Subject<void>();

  constructor(
    private cajaService: CajaService,
    private authService: AuthService,
    private formBuilder: FormBuilder
  ) {
    this.aperturaForm = this.formBuilder.group({
      cash_register_id: ['', Validators.required],
      opening_amount: ['', [Validators.required, Validators.min(0)]],
      notes: ['']
    });
  }

  ngOnInit(): void {
    this.checkUserRole();
    this.loadCashRegisters();
    this.loadAperturas();
    this.loadActiveSession();
    
    // Suscribirse a cambios de sesión activa
    this.cajaService.activeSession$
      .pipe(takeUntil(this.destroy$))
      .subscribe(session => {
        this.activeSession = session;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  checkUserRole(): void {
    this.authService.currentUser$
      .pipe(takeUntil(this.destroy$))
      .subscribe(user => {
        if (user) {
          this.isAdmin = user.role === 'ADMIN';
          this.isCajero = user.role === 'CAJERO';
        }
      });
  }

  loadCashRegisters(): void {
    this.cajaService.getCashRegisters(true)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.cashRegisters = response.data || [];
          // Si es cajero, auto-asignar la primera caja activa
          if (this.isCajero && this.cashRegisters.length > 0) {
            this.aperturaForm.patchValue({
              cash_register_id: this.cashRegisters[0].id
            });
          }
        },
        error: (error) => {
          console.error('Error al cargar cajas:', error);
        }
      });
  }

  loadAperturas(): void {
    this.loading = true;
    // Si statusFilter es 'todas', enviar undefined para obtener todas
    const status = this.statusFilter === 'todas' ? undefined : this.statusFilter;
    this.cajaService.listSessions(0, 100, status)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.aperturas = data;
          this.loading = false;
        },
        error: (error) => {
          this.errorMessage = 'Error al cargar aperturas: ' + (error.error?.detail || error.message);
          this.loading = false;
        }
      });
  }

  loadActiveSession(): void {
    this.cajaService.getActiveSession()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (session) => {
          this.activeSession = session;
          this.cajaService.updateActiveSession();
        },
        error: () => {
          this.activeSession = null;
        }
      });
  }

  onAbrirCaja(): void {
    if (this.activeSession) {
      this.errorMessage = 'Ya existe una caja abierta. Debe cerrarla primero.';
      return;
    }
    this.showForm = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  onSubmit(): void {
    if (!this.aperturaForm.valid) {
      this.errorMessage = 'Por favor completa todos los campos requeridos';
      return;
    }

    this.loading = true;
    this.cajaService.openSession(this.aperturaForm.value)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (session) => {
          this.successMessage = `Caja abierta exitosamente a las ${new Date(session.opening_date).toLocaleTimeString()}`;
          this.activeSession = session;
          this.cajaService.updateActiveSession();
          this.aperturaForm.reset();
          this.showForm = false;
          this.loadAperturas();
          this.loading = false;
        },
        error: (error) => {
          this.errorMessage = 'Error al abrir caja: ' + (error.error?.detail || error.message);
          this.loading = false;
        }
      });
  }

  onCancel(): void {
    this.showForm = false;
    this.aperturaForm.reset();
    this.errorMessage = '';
  }

  onCerrar(session: CashSession): void {
    if (confirm(`¿Está seguro que desea cerrar la caja abierta a las ${new Date(session.opening_date).toLocaleTimeString()}?`)) {
      window.location.href = `/caja/cierre?session_id=${session.id}`;
    }
  }

  filteredAperturas(): CashSession[] {
    let filtered = this.aperturas;
    
    if (this.searchTerm) {
      const term = this.searchTerm.toLowerCase();
      filtered = filtered.filter(a => 
        (a.user?.first_name + ' ' + a.user?.last_name).toLowerCase().includes(term) ||
        new Date(a.opening_date).toLocaleString().includes(this.searchTerm)
      );
    }

    return filtered;
  }

  get totalPages(): number {
    return Math.ceil(this.filteredAperturas().length / this.itemsPerPage);
  }

  get paginatedAperturas(): CashSession[] {
    const filtered = this.filteredAperturas();
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return filtered.slice(start, start + this.itemsPerPage);
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  prevPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  changeStatusFilter(status: 'todas' | 'abierta' | 'cerrada'): void {
    this.statusFilter = status;
    this.currentPage = 1;
    this.loadAperturas();
  }

  clearMessages(): void {
    this.errorMessage = '';
    this.successMessage = '';
  }

  get hasCashRegisterError(): boolean {
    return (this.aperturaForm.get('cash_register_id')?.invalid && this.aperturaForm.get('cash_register_id')?.touched) || false;
  }

  get hasOpeningAmountError(): boolean {
    return (this.aperturaForm.get('opening_amount')?.invalid && this.aperturaForm.get('opening_amount')?.touched) || false;
  }
}
