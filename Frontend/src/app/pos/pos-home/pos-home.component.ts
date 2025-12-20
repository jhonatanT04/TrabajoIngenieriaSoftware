import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { InventarioService } from '../../core/services/inventario.service';
@Component({
  standalone: true,
  selector: 'app-pos-home',
  imports: [CommonModule, FormsModule],
  templateUrl: './pos-home.component.html',
  styleUrls: ['./pos-home.component.css']
})
export class PosHomeComponent implements OnInit {

  search = '';
  carrito: any[] = [];
  productos: any[] = [];

  constructor(
    private router: Router,
    private inventario: InventarioService
  ) {}

  ngOnInit() {
    this.productos = this.inventario.getProductos();
  }

  agregar(producto: any) {
    if (producto.stock <= 0) return;

    const item = this.carrito.find(p => p.id === producto.id);

    if (item) {
      if (item.cantidad < producto.stock) {
        item.cantidad++;
      }
    } else {
      this.carrito.push({
        ...producto,
        cantidad: 1
      });
    }
  }

  sumar(item: any) {
    if (item.cantidad < item.stock) {
      item.cantidad++;
    }
  }

  restar(item: any) {
    if (item.cantidad > 1) {
      item.cantidad--;
    }
  }

  eliminar(item: any) {
    this.carrito = this.carrito.filter(p => p.id !== item.id);
  }

  total() {
    return this.carrito.reduce(
      (acc, p) => acc + p.precio * p.cantidad, 0
    );
  }

  irAPago() {
    this.router.navigate(['/pos/pago'], {
      state: { carrito: this.carrito }
    });
  }
}
