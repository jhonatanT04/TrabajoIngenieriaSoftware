import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-admin-dashboard',
  imports: [CommonModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent {

  metrics = [
    {
      label: 'Ventas Hoy',
      value: '$12,450',
      icon: 'attach_money',
      type: 'success',
      change: '+12.5% vs ayer',
      changeType: 'positive'
    },
    {
      label: 'Productos',
      value: '340',
      icon: 'inventory_2',
      type: 'primary',
      change: '+5 esta semana',
      changeType: 'positive'
    },
    {
      label: 'Usuarios',
      value: '24',
      icon: 'people',
      type: 'info',
      change: '+2 nuevos',
      changeType: 'positive'
    },
    {
      label: 'Proveedores',
      value: '18',
      icon: 'local_shipping',
      type: 'warning',
      change: 'Sin cambios',
      changeType: 'positive'
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

  recentActivity = [
    {
      title: 'Venta #1234 completada',
      description: 'Usuario: Juan Pérez - Total: $450.00',
      time: 'Hace 5 min'
    },
    {
      title: 'Nuevo producto agregado',
      description: 'Producto: Coca Cola 2L - Stock: 50 unidades',
      time: 'Hace 15 min'
    },
    {
      title: 'Inventario actualizado',
      description: 'Se actualizaron 25 productos',
      time: 'Hace 1 hora'
    },
    {
      title: 'Usuario creado',
      description: 'Nuevo cajero: María González',
      time: 'Hace 2 horas'
    },
    {
      title: 'Cierre de caja',
      description: 'Caja #1 - Total: $3,450.00',
      time: 'Hace 3 horas'
    }
  ];

  constructor(private router: Router) {}
}
