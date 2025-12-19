import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ParametrosService } from '../../../core/services/parametros.service';

@Component({
  standalone: true,
  selector: 'app-descuentos',
  imports: [CommonModule, FormsModule],
  templateUrl: './descuentos.component.html'
})
export class DescuentosComponent {

  descuento!: number;

  constructor(private param: ParametrosService) {
    this.descuento = this.param.descuentoGlobal;
  }

  guardar() {
    this.param.setDescuento(this.descuento);
  }
}
