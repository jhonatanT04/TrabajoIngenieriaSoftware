import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-cajero-dashboard',
  imports: [CommonModule],
  templateUrl: './cajero-dashboard.component.html',
  styleUrls: ['./cajero-dashboard.component.css']
})
export class CajeroDashboardComponent {

  metrics = [
    {
      label: 'Ventas Hoy',
      value: '$3,245',
      icon: 'point_of_sale',
      type: 'success',
      change: '+8 ventas',
      changeType: 'positive'
    },
    {
      label: 'Efectivo en Caja',
      value: '$2,890',
      icon: 'account_balance_wallet',
      type: 'primary',
      change: 'Caja abierta',
      changeType: 'positive'
    },
    {
      label: 'Clientes Atendidos',
      value: '32',
      icon: 'people',
      type: 'info',
      change: '+5 nuevos',
      changeType: 'positive'
    },
    {
      label: 'Productos Vendidos',
      value: '124',
      icon: 'inventory_2',
      type: 'warning',
      change: 'Hoy',
      changeType: 'positive'
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

  recentActivity = [
    {
      title: 'Venta #1245 completada',
      description: 'Cliente: Ana García - Total: $125.50',
      time: 'Hace 2 min'
    },
    {
      title: 'Cliente nuevo registrado',
      description: 'Pedro Martínez - Teléfono: 555-1234',
      time: 'Hace 15 min'
    },
    {
      title: 'Venta #1244 completada',
      description: 'Cliente: María López - Total: $89.00',
      time: 'Hace 30 min'
    },
    {
      title: 'Producto agotado',
      description: 'Coca Cola 2L - Solicitar reposición',
      time: 'Hace 1 hora'
    },
    {
      title: 'Venta #1243 completada',
      description: 'Cliente: Juan Pérez - Total: $210.00',
      time: 'Hace 2 horas'
    }
  ];

  constructor(private router: Router) {}
}
