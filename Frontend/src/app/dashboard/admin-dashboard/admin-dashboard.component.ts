import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { DashboardService } from '../../core/services/dashboard.service';
import { ProductoService } from '../../core/services/producto.service';
import { UsuariosService } from '../../core/services/usuarios.service';
import { ProveedorService } from '../../core/services/proveedor.service';

@Component({
  standalone: true,
  selector: 'app-admin-dashboard',
  imports: [CommonModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {

  metrics = [
    {
      label: 'Ventas Hoy',
      value: '$0',
      icon: 'attach_money',
      type: 'success',
      change: 'Cargando...',
      changeType: 'neutral'
    },
    {
      label: 'Productos',
      value: '0',
      icon: 'inventory_2',
      type: 'primary',
      change: 'Cargando...',
      changeType: 'neutral'
    },
    {
      label: 'Usuarios',
      value: '0',
      icon: 'people',
      type: 'info',
      change: 'Cargando...',
      changeType: 'neutral'
    },
    {
      label: 'Proveedores',
      value: '0',
      icon: 'local_shipping',
      type: 'warning',
      change: 'Cargando...',
      changeType: 'neutral'
    }
  ];

  quickActions = [
    {
      title: 'Nueva Venta',
      icon: 'add_shopping_cart',
      action: () => this.router.navigate(['/pos'])
    },
    {
      title: 'Nuevo Producto',
      icon: 'add_box',
      action: () => this.router.navigate(['/productos/create'])
    },
    {
      title: 'Nuevo Usuario',
      icon: 'person_add',
      action: () => this.router.navigate(['/admin/usuarios/create'])
    },
    {
      title: 'Reportes',
      icon: 'assessment',
      action: () => this.router.navigate(['/reportes'])
    }
  ];

  recentActivity: any[] = [];

  constructor(
    private router: Router,
    private dashboardService: DashboardService,
    private productoService: ProductoService,
    private usuariosService: UsuariosService,
    private proveedorService: ProveedorService
  ) {}

  ngOnInit(): void {
    this.loadMetrics();
    this.loadRecentActivity();
  }

  loadMetrics(): void {
    // Cargar productos
    this.productoService.getAll().subscribe({
      next: (productos) => {
        this.metrics[1].value = productos.length.toString();
        this.metrics[1].change = `${productos.length} en inventario`;
        this.metrics[1].changeType = 'positive';
      },
      error: (err) => {
        console.error('Error cargando productos:', err);
        this.metrics[1].change = 'Error al cargar';
        this.metrics[1].changeType = 'neutral';
      }
    });

    // Cargar usuarios
    this.usuariosService.getAll().subscribe({
      next: (usuarios) => {
        this.metrics[2].value = usuarios.length.toString();
        this.metrics[2].change = `${usuarios.length} usuarios activos`;
        this.metrics[2].changeType = 'positive';
      },
      error: (err) => {
        console.error('Error cargando usuarios:', err);
        this.metrics[2].change = 'Error al cargar';
        this.metrics[2].changeType = 'neutral';
      }
    });

    // Cargar proveedores
    this.proveedorService.getAll().subscribe({
      next: (proveedores) => {
        this.metrics[3].value = proveedores.length.toString();
        this.metrics[3].change = `${proveedores.length} proveedores`;
        this.metrics[3].changeType = 'positive';
      },
      error: (err) => {
        console.error('Error cargando proveedores:', err);
        this.metrics[3].change = 'Error al cargar';
        this.metrics[3].changeType = 'neutral';
      }
    });

    // Métricas de dashboard (ventas, etc.)
    this.dashboardService.getMetrics().subscribe({
      next: (data) => {
        this.metrics[0].value = `$${data.ventas_hoy.toLocaleString()}`;
        this.metrics[0].change = 'Ventas de hoy';
        this.metrics[0].changeType = 'positive';
      },
      error: (err) => {
        console.error('Error cargando métricas:', err);
      }
    });
  }

  loadRecentActivity(): void {
    this.dashboardService.getRecentActivity(10).subscribe({
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
