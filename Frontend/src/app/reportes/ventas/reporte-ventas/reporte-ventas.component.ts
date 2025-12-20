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

  constructor(private reportes: ReportesService) {}

  ngOnInit() {
    this.ventas = this.reportes.reporteVentas();
  }
}
