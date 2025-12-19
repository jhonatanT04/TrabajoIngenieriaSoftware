import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MovimientosService } from '../../../core/services/movimientos.service';

@Component({
  standalone: true,
  selector: 'app-movimiento-list',
  imports: [CommonModule],
  templateUrl: './movimiento-list.component.html'
})
export class MovimientoListComponent implements OnInit {

  movimientos: any[] = [];

  constructor(private movimientosService: MovimientosService) {}

  ngOnInit() {
    this.movimientos = this.movimientosService.getAll();
  }
}
