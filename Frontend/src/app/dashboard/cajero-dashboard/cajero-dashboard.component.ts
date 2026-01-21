import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { DashboardService } from '../../core/services/dashboard.service';

@Component({
  standalone: true,
  selector: 'app-cajero-dashboard',
  imports: [CommonModule],
  templateUrl: './cajero-dashboard.component.html',
  styleUrls: ['./cajero-dashboard.component.css']
})
export class CajeroDashboardComponent implements OnInit {

  metrics = [
    {
      label: 'Ventas Hoy',
      value: '$0',
      icon: 'point_of_sale',
      type: 'success',
      change: 'Cargando...',
      changeType: 'neutral'
    },
    {
      label: 'Efectivo en Caja',
      value: '$0',
      icon: 'account_balance_wallet',
      type: 'primary',
      change: 'Verificando...',
      changeType: 'neutral'
    },
    {
      label: 'Clientes Atendidos',
      value: '0',
      icon: 'people',
      type: 'info',
      change: 'Cargando...',
      changeType: 'neutral'
    },
    {
      label: 'Productos Vendidos',
      value: '0',
      icon: 'inventory_2',
      type: 'warning',
      change: 'Hoy',
      changeType: 'neutral'
    }
  ];

  quickActions = [
    {
      title: 'Punto de Venta',
      icon: 'shopping_cart',
      action: () => this.router.navigate(['/pos'])
    },
    {
      title: 'Nueva Venta',
      icon: 'add_shopping_cart',
      action: () => this.router.navigate(['/ventas/nuevo'])
    },
    {
      title: 'Nuevo Cliente',
      icon: 'person_add',
      action: () => this.router.navigate(['/clientes/nuevo'])
    },
    {
      title: 'Ver Caja',
      icon: 'account_balance',
      action: () => this.router.navigate(['/caja'])
    }
  ];

  recentActivity: any[] = [];

  constructor(
    private router: Router,
    private dashboardService: DashboardService
  ) {}

  ngOnInit(): void {
    this.loadMetrics();
    this.loadRecentActivity();
  }

  loadMetrics(): void {
    this.dashboardService.getMetrics().subscribe({
      next: (data) => {
        this.metrics[0].value = `$${data.ventas_hoy.toLocaleString()}`;
        this.metrics[0].change = 'Ventas de hoy';
        this.metrics[0].changeType = 'positive';
      },
      error: (err) => {
        console.error('Error cargando métricas:', err);
        this.metrics[0].change = 'Error al cargar';
        this.metrics[0].changeType = 'neutral';
      }
    });
  }

  loadRecentActivity(): void {
    this.dashboardService.getRecentActivity(5).subscribe({
      next: (activity) => {
        this.recentActivity = activity;
      },
      error: (err) => {
        console.error('Error cargando actividad reciente:', err);
        this.recentActivity = [];
      }
    });
  }
}
