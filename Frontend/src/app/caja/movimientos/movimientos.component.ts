import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CajaService, CashSession, CashTransaction } from '../../core/services/caja.service';

@Component({
  standalone: true,
  selector: 'app-movimientos-caja',
  imports: [CommonModule],
  templateUrl: './movimientos.component.html'
})
export class MovimientosCajaComponent implements OnInit {
  currentSession: CashSession | null = null;
  movimientos: CashTransaction[] = [];
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
          this.loadMovimientos(this.currentSession.id);
        }
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  loadMovimientos(sessionId: string) {
    this.cajaService.getSessionTransactions(sessionId).subscribe({
      next: (transactions) => this.movimientos = transactions
    });
  }

  getMovimientos() {
    return this.movimientos;
  }
}
