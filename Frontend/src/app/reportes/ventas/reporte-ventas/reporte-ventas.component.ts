import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportesService } from '../../services/reportes.service';

@Component({
  standalone: true,
  selector: 'app-reporte-ventas',
  imports: [CommonModule],
  templateUrl: './reporte-ventas.component.html'
})
export class ReporteVentasComponent implements OnInit {
  ventas: any[] = [];
  loading = false;

  constructor(private reportes: ReportesService) {}

  ngOnInit() {
    this.loading = true;
    this.reportes.reporteVentas().subscribe({
      next: (data) => {
        this.ventas = data;
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }
}
