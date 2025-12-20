import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-venta-create',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './venta-create.component.html',
  styleUrls: ['./venta-create.component.css']
})
export class VentaCreateComponent {
  venta = {
    cliente: '',
    fecha: new Date().toISOString().slice(0, 10),
    monto: 0,
    estado: 'Pendiente',
    vendedor: '',
    notas: ''
  };

  guardar(): void {
    alert('Venta guardada (demo)');
  }

  cancelar(): void {
    history.back();
  }
}
