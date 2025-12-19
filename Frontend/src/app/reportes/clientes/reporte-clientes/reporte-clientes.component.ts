import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportesService } from '../../services/reportes.service';

@Component({
  standalone: true,
  selector: 'app-reporte-clientes',
  imports: [CommonModule],
  templateUrl: './reporte-clientes.component.html'
})
export class ReporteClientesComponent implements OnInit {

  clientes: any[] = [];

  constructor(private reportes: ReportesService) {}

  ngOnInit(): void {
    this.clientes = this.reportes.reporteClientes();
  }
}
