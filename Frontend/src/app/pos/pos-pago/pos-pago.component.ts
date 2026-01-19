import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { PosProducto } from '../../core/models/pos-product.model';
import { VentaService } from '../../core/services/venta.service';

@Component({
  standalone: true,
  selector: 'app-pos-pago',
  imports: [CommonModule, FormsModule],
  templateUrl: './pos-pago.component.html',
  styleUrls: ['./pos-pago.component.css']
})
export class PosPagoComponent {
  carrito: PosProducto[] = history.state.carrito || [];
  efectivo: number = 0;
  loading = false;

  constructor(
    private router: Router,
    private ventaService: VentaService
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

    // TODO: Implementar creación de venta en el backend
    // Por ahora solo navegamos al ticket
    this.router.navigate(['/pos/ticket'], {
      state: {
        carrito: this.carrito,
        total: totalVenta,
        efectivo: this.efectivo,
        vuelto: this.vuelto()
      }
    });
  }

  cancelar(): void {
    this.router.navigate(['/pos']);
  }
}
