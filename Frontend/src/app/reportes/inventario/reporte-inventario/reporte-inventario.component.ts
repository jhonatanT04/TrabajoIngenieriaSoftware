import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportesService } from '../../services/reportes.service';

@Component({
  standalone: true,
  selector: 'app-reporte-inventario',
  imports: [CommonModule],
  templateUrl: './reporte-inventario.component.html'
})
export class ReporteInventarioComponent implements OnInit {
  movimientos: any[] = [];
  loading = false;

  constructor(private reportes: ReportesService) {}

  ngOnInit() {
    this.loading = true;
    this.reportes.reporteInventario().subscribe({
      next: (data) => {
        this.movimientos = data;
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }
}
