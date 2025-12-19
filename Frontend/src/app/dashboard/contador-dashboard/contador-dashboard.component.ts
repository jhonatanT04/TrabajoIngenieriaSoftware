import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-contador-dashboard',
  imports: [CommonModule],
  templateUrl: './contador-dashboard.component.html'
})
export class ContadorDashboardComponent {
  metrics = [
    { label: 'Cierres de caja', value: 3 },
    { label: 'Ventas del mes', value: '$8.450' },
    { label: 'Diferencias detectadas', value: 1 }
  ];
}
