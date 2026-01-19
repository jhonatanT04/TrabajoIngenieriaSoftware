import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { InventarioService } from '../../../core/services/inventario.service';
import { ProductoService } from '../../../core/services/producto.service';

@Component({
  standalone: true,
  selector: 'app-stock-ajuste',
  imports: [CommonModule, FormsModule],
  templateUrl: './stock-ajuste.component.html'
})
export class StockAjusteComponent implements OnInit {
  producto: any;
  cantidad = 0;
  razon = '';
  loading = false;
  productId = '';

  constructor(
    private route: ActivatedRoute,
    private inventario: InventarioService,
    private productoService: ProductoService,
    private router: Router
  ) {
    this.productId = route.snapshot.paramMap.get('id')!;
  }

  ngOnInit() {
    this.loadProduct();
  }

  loadProduct() {
    this.loading = true;
    this.productoService.getById(this.productId).subscribe({
      next: (producto) => {
        this.producto = producto;
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  ajustar() {
    if (!this.razon) {
      alert('Debe ingresar una razón para el ajuste');
      return;
    }

    this.loading = true;
    this.inventario.adjustInventory({
      product_id: this.productId,
      new_quantity: this.cantidad,
      reason: this.razon
    }).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/inventario/stock']);
      },
      error: () => this.loading = false
    });
  }
}
