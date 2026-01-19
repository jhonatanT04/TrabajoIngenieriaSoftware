import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CajaService, CashSession } from '../../core/services/caja.service';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-cierre',
  imports: [CommonModule, FormsModule],
  templateUrl: './cierre.component.html'
})
export class CierreComponent implements OnInit {
  currentSession: CashSession | null = null;
  actualClosingAmount = 0;
  notes = '';
  loading = false;

  constructor(
    public cajaService: CajaService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadCurrentSession();
  }

  loadCurrentSession() {
    this.loading = true;
    this.cajaService.getSessions({ status: 'abierta' }).subscribe({
      next: (sessions) => {
        if (sessions.length > 0) {
          this.currentSession = sessions[0];
        }
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  getEstado() {
    if (!this.currentSession) {
      return { abierta: false, total: 0 };
    }
    return { abierta: true, total: this.currentSession.expected_closing_amount };
  }

  cerrar() {
    if (!this.currentSession) return;

    this.loading = true;
    this.cajaService.closeSession(this.currentSession.id, {
      actual_closing_amount: this.actualClosingAmount,
      notes: this.notes
    }).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/dashboard']);
      },
      error: () => this.loading = false
    });
  }
}
