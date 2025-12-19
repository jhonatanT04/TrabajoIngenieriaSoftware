import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportesService } from '../../services/reportes.service';

@Component({
  standalone: true,
  selector: 'app-reporte-caja',
  imports: [CommonModule],
  templateUrl: './reporte-caja.component.html'
})
export class ReporteCajaComponent implements OnInit {

  estado: any;

  constructor(private reportes: ReportesService) {}

  ngOnInit(): void {
    this.estado = this.reportes.reporteCaja();
  }
}
