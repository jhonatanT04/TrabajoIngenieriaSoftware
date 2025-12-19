import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { InventarioService } from '../../../core/services/inventario.service';
import { MovimientosService } from '../../../core/services/movimientos.service';

@Component({
  standalone: true,
  selector: 'app-stock-ajuste',
  imports: [CommonModule, FormsModule],
  templateUrl: './stock-ajuste.component.html'
})
export class StockAjusteComponent {

  producto: any;
  cantidad = 0;

  constructor(
    route: ActivatedRoute,
    private inventario: InventarioService,
    private movimientos: MovimientosService,
    private router: Router
  ) {
    this.producto = this.inventario.getById(+route.snapshot.paramMap.get('id')!);
  }

  ajustar() {
    this.inventario.ajustarStock(this.producto.id, this.cantidad);
    this.movimientos.registrar('ENTRADA', this.producto.nombre, this.cantidad);
    this.router.navigate(['/inventario/stock']);
  }
}
