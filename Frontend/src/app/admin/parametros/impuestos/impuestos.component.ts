import { Component } from '@angular/core'; // ✅ Component
import { CommonModule } from '@angular/common'; // ✅ CommonModule
import { FormsModule } from '@angular/forms'; // ✅ FormsModule
import { ParametrosService } from '../../../core/services/parametros.service'; // ✅ tu servicio

@Component({
  standalone: true, // ✅ Standalone
  selector: 'app-impuestos',
  imports: [CommonModule, FormsModule], // ✅ Importar módulos necesarios
  templateUrl: './impuestos.component.html'
})
export class ImpuestosComponent {

  impuesto: number; // declaración antes de usar

  constructor(private param: ParametrosService) {
    this.impuesto = this.param.impuesto; // inicialización correcta
  }

  guardar() {
    this.param.setImpuesto(this.impuesto);
    alert(`Impuesto actualizado a ${this.impuesto * 100}%`);
  }
}
