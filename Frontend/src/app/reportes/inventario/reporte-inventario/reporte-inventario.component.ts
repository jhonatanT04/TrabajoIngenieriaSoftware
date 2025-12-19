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

  constructor(private reportes: ReportesService) {}

  ngOnInit() {
    this.movimientos = this.reportes.reporteInventario();
  }
}
