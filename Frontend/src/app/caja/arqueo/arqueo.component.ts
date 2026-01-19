import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CajaService, CashSession, CashTransaction } from '../../core/services/caja.service';

@Component({
  standalone: true,
  selector: 'app-arqueo',
  imports: [CommonModule],
  templateUrl: './arqueo.component.html'
})
export class ArqueoComponent implements OnInit {
  currentSession: CashSession | null = null;
  transactions: CashTransaction[] = [];
  loading = false;

  constructor(public cajaService: CajaService) {}

  ngOnInit() {
    this.loadCurrentSession();
  }

  loadCurrentSession() {
    this.loading = true;
    this.cajaService.getSessions({ status: 'abierta' }).subscribe({
      next: (sessions) => {
        if (sessions.length > 0) {
          this.currentSession = sessions[0];
          this.loadTransactions(this.currentSession.id);
        }
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  loadTransactions(sessionId: string) {
    this.cajaService.getSessionTransactions(sessionId).subscribe({
      next: (transactions) => this.transactions = transactions
    });
  }

  getEstado() {
    if (!this.currentSession) {
      return { abierta: false, montoInicial: 0, ventas: 0, total: 0 };
    }

    const ventas = this.transactions
      .filter(t => t.transaction_type === 'venta')
      .reduce((sum, t) => sum + t.amount, 0);

    const total = this.currentSession.opening_amount + ventas;

    return {
      abierta: true,
      montoInicial: this.currentSession.opening_amount,
      ventas,
      total
    };
  }
}
