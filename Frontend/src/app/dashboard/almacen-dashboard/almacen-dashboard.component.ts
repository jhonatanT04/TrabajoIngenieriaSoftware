import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../core/services/dashboard.service';
import { ProductoService } from '../../core/services/producto.service';

@Component({
  standalone: true,
  selector: 'app-almacen-dashboard',
  imports: [CommonModule],
  templateUrl: './almacen-dashboard.component.html'
})
export class AlmacenDashboardComponent implements OnInit {
  metrics = [
    { label: 'Productos bajos de stock', value: 0 },
    { label: 'Total productos', value: 0 },
    { label: 'Movimientos hoy', value: 0 }
  ];

  constructor(
    private dashboardService: DashboardService,
    private productoService: ProductoService
  ) {}

  ngOnInit(): void {
    this.loadMetrics();
  }

  loadMetrics(): void {
    this.dashboardService.getMetrics().subscribe({
      next: (data) => {
        this.metrics[0].value = data.stock_bajo;
        this.metrics[1].value = data.total_productos;
      },
      error: (err) => {
        console.error('Error cargando métricas de almacén:', err);
      }
    });
  }
}
