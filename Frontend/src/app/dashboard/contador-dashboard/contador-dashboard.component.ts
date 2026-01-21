import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../core/services/dashboard.service';

@Component({
  standalone: true,
  selector: 'app-contador-dashboard',
  imports: [CommonModule],
  templateUrl: './contador-dashboard.component.html'
})
export class ContadorDashboardComponent implements OnInit {
  metrics = [
    { label: 'Ventas del día', value: '$0' },
    { label: 'Ventas del mes', value: '$0' },
    { label: 'Total clientes', value: 0 }
  ];

  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.loadMetrics();
  }

  loadMetrics(): void {
    this.dashboardService.getMetrics().subscribe({
      next: (data) => {
        this.metrics[0].value = `$${data.ventas_hoy.toLocaleString()}`;
        this.metrics[2].value = data.total_clientes;
      },
      error: (err) => {
        console.error('Error cargando métricas de contador:', err);
      }
    });

    this.dashboardService.getSalesSummary(30).subscribe({
      next: (data) => {
        this.metrics[1].value = `$${data.total_sales.toLocaleString()}`;
      },
      error: (err) => {
        console.error('Error cargando resumen de ventas:', err);
      }
    });
  }
}
