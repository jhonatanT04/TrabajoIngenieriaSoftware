import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { DashboardService } from '../../core/services/dashboard.service';
import { VentaService } from '../../core/services/venta.service';
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
      action: () => this.navigateNuevaVenta()
    },
    {
      title: 'Nuevo Producto',
      icon: 'add_box',
      action: () => this.router.navigate(['/productos/nuevo'])
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

  // Datos para gráficos sencillos sin librerías externas
  ventasPorDia: { label: string; total: number }[] = [];
  topProductos: { name: string; cantidad: number }[] = [];
  maxVentasDia = 1;
  maxProductoCantidad = 1;
  totalVentas7Dias = 0;
  totalItemsTop = 0;

  constructor(
    private router: Router,
    private dashboardService: DashboardService,
    private ventaService: VentaService,
    private productoService: ProductoService,
    private usuariosService: UsuariosService,
    private proveedorService: ProveedorService
  ) {}

  ngOnInit(): void {
    this.loadMetrics();
    this.loadRecentActivity();
    this.loadCharts();
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

  private navigateNuevaVenta(): void {
    // Navegar al formulario estándar de nueva venta
    this.router.navigate(['/ventas/nuevo']);
  }

  private loadCharts(): void {
    // Cargar ventas y calcular resumen para gráficos
    this.ventaService.getAll({ limit: 500 }).subscribe({
      next: (ventas: any[]) => {
        // Ventas por día (últimos 7 días)
        const hoy = new Date();
        const mapa: Record<string, number> = {};
        for (let i = 6; i >= 0; i--) {
          const d = new Date(hoy);
          d.setDate(hoy.getDate() - i);
          const key = d.toISOString().slice(0, 10);
          mapa[key] = 0;
        }
        ventas.forEach(v => {
          const key = (v.sale_date || '').slice(0, 10);
          if (mapa[key] !== undefined) {
            mapa[key] += Number(v.total_amount || 0);
          }
        });
        this.ventasPorDia = Object.keys(mapa).map(k => ({ label: k.slice(5), total: mapa[k] }));
        this.maxVentasDia = Math.max(...this.ventasPorDia.map(v => v.total), 1);
        this.totalVentas7Dias = this.ventasPorDia.reduce((acc, v) => acc + v.total, 0);

        // Top productos por cantidad vendida
        const prodMap: Record<string, { name: string; cantidad: number }> = {};
        ventas.forEach(v => {
          (v.items || []).forEach((it: any) => {
            const id = it.product_id;
            if (!id) return; // evitar agregar sin identificador
            const name = it.product_name || it.product?.name || it.product?.nombre || 'Producto sin nombre';
            if (!prodMap[id]) prodMap[id] = { name, cantidad: 0 };
            prodMap[id].cantidad += Number(it.quantity || 0);
          });
        });
        this.topProductos = Object.values(prodMap)
          .sort((a, b) => b.cantidad - a.cantidad)
          .slice(0, 5);
        this.maxProductoCantidad = Math.max(...this.topProductos.map(p => p.cantidad), 1);
        this.totalItemsTop = this.topProductos.reduce((acc, p) => acc + p.cantidad, 0);
      },
      error: (err) => {
        console.error('Error cargando ventas para gráficos:', err);
        this.ventasPorDia = [];
        this.topProductos = [];
      }
    });
  }
}
