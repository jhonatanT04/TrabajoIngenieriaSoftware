import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CajaService } from '../../core/services/caja.service';

@Component({
  standalone: true,
  selector: 'app-movimientos-caja',
  imports: [CommonModule],
  templateUrl: './movimientos.component.html'
})
export class MovimientosCajaComponent {

  constructor(public cajaService: CajaService) {}
}
