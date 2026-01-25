import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { DashboardService } from '../../core/services/dashboard.service';
import { VentaService } from '../../core/services/venta.service';

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
      action: () => this.router.navigate(['/clientes/create'])
    },
    {
      title: 'Ver Caja',
      icon: 'account_balance',
      action: () => this.router.navigate(['/caja'])
    }
  ];

  recentActivity: any[] = [];

  // Gráficos
  ventasPorHora: { label: string; total: number }[] = [];
  maxVentasHora = 1;
  totalVentasHoy = 0;
  
  efectivoVsTarjeta: { type: string; total: number; percentage: number }[] = [
    { type: 'Efectivo', total: 0, percentage: 0 },
    { type: 'Tarjeta', total: 0, percentage: 0 }
  ];

  constructor(
    private router: Router,
    private dashboardService: DashboardService,
    private ventaService: VentaService
  ) {}

  ngOnInit(): void {
    this.loadMetrics();
    this.loadRecentActivity();
    this.loadCharts();
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

  loadCharts(): void {
    this.ventaService.getAll().subscribe({
      next: (ventas: any[]) => {
        const hoy = new Date().toISOString().slice(0, 10);
        const ventasHoy = ventas.filter(v => (v.sale_date || '').slice(0, 10) === hoy);

        // Ventas por hora
        const horaMap: Record<string, number> = {};
        for (let i = 0; i < 24; i++) {
          const hora = String(i).padStart(2, '0');
          horaMap[hora] = 0;
        }
        ventasHoy.forEach(v => {
          const hora = (v.sale_date || '').slice(11, 13);
          if (horaMap[hora] !== undefined) {
            horaMap[hora] += Number(v.total_amount || 0);
          }
        });
        this.ventasPorHora = Object.keys(horaMap)
          .map(k => ({ label: k + ':00', total: horaMap[k] }))
          .filter(v => v.total > 0);
        
        if (this.ventasPorHora.length === 0) {
          this.ventasPorHora = [{ label: '0:00', total: 0 }];
        }
        this.maxVentasHora = Math.max(...this.ventasPorHora.map(v => v.total), 1);
        this.totalVentasHoy = this.ventasPorHora.reduce((acc, v) => acc + v.total, 0);

        // Efectivo vs Tarjeta
        let totalEfectivo = 0;
        let totalTarjeta = 0;
        ventasHoy.forEach(v => {
          if (v.payment_method === 'Efectivo' || v.payment_method === 'cash') {
            totalEfectivo += Number(v.total_amount || 0);
          } else if (v.payment_method === 'Tarjeta' || v.payment_method === 'card') {
            totalTarjeta += Number(v.total_amount || 0);
          }
        });
        const totalPago = totalEfectivo + totalTarjeta || 1;
        this.efectivoVsTarjeta[0].total = totalEfectivo;
        this.efectivoVsTarjeta[0].percentage = (totalEfectivo / totalPago) * 100;
        this.efectivoVsTarjeta[1].total = totalTarjeta;
        this.efectivoVsTarjeta[1].percentage = (totalTarjeta / totalPago) * 100;
      },
      error: (err) => {
        console.error('Error cargando datos de gráficos:', err);
      }
    });
  }}