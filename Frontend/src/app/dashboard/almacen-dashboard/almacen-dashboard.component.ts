import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-almacen-dashboard',
  imports: [CommonModule],
  templateUrl: './almacen-dashboard.component.html'
})
export class AlmacenDashboardComponent {
  metrics = [
    { label: 'Productos bajos de stock', value: 12 },
    { label: 'Recepciones pendientes', value: 4 },
    { label: 'Productos por vencer', value: 6 }
  ];
}
