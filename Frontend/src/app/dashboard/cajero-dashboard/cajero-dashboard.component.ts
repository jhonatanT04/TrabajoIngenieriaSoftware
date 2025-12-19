import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-cajero-dashboard',
  imports: [CommonModule],
  templateUrl: './cajero-dashboard.component.html'
})
export class CajeroDashboardComponent {
  metrics = [
    { label: 'Ventas hoy', value: 23 },
    { label: 'Total vendido', value: '$540' },
    { label: 'Caja actual', value: '$320' }
  ];
}
