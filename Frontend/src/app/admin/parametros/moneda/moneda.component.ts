import { Component } from '@angular/core'; // necesario
import { CommonModule } from '@angular/common'; // necesario
import { FormsModule } from '@angular/forms'; // necesario para [(ngModel)]
import { ParametrosService } from '../../../core/services/parametros.service';

@Component({
  selector: 'app-moneda',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './moneda.component.html'
})
export class MonedaComponent {

  moneda: string; // declaramos propiedad antes de usar

  constructor(private paramService: ParametrosService) {
    this.moneda = this.paramService.moneda; // inicializamos
  }

  guardar() {
    this.paramService.setMoneda(this.moneda);
    alert('Moneda actualizada a: ' + this.moneda);
  }
}
