import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { PosProducto } from '../../core/models/pos-product.model';
import { CajaService } from '../../core/services/caja.service';

@Component({
  standalone: true,
  selector: 'app-pos-pago',
  imports: [CommonModule, FormsModule],
  templateUrl: './pos-pago.component.html'
})
export class PosPagoComponent {

  carrito: PosProducto[] = history.state.carrito || [];
  efectivo: number = 0;

  constructor(
    private router: Router,
    private cajaService: CajaService
  ) {}

  total(): number {
    return this.carrito.reduce(
      (acumulado, producto) =>
        acumulado + producto.precio * producto.cantidad,
      0
    );
  }

  vuelto(): number {
    return this.efectivo - this.total();
  }

  pagar(): void {
    const totalVenta = this.total();

    // 🔥 REGISTRAR MOVIMIENTO EN CAJA
    this.cajaService.registrarVenta(totalVenta);

    // 👉 IR AL TICKET
    this.router.navigate(['/pos/ticket'], {
      state: {
        carrito: this.carrito,
        total: totalVenta,
        efectivo: this.efectivo,
        vuelto: this.vuelto()
      }
    });
  }
}
