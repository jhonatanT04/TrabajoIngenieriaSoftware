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
  loading = false;

  constructor(private reportes: ReportesService) {}

  ngOnInit(): void {
    this.loading = true;
    this.reportes.reporteClientes().subscribe({
      next: (data) => {
        this.clientes = data;
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }
}
