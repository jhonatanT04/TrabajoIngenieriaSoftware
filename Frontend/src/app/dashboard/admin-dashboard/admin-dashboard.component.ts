import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-admin-dashboard',
  imports: [CommonModule],
  templateUrl: './admin-dashboard.component.html'
})
export class AdminDashboardComponent {
  metrics = [
    { label: 'Ventas del día', value: '$1.250' },
    { label: 'Productos', value: 340 },
    { label: 'Proveedores', value: 18 },
    { label: 'Usuarios', value: 6 }
  ];
}
