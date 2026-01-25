import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ProductoService } from '../../core/services/producto.service';
import { AuthService } from '../../core/services/auth.service';
import { PosCartService, PosCartItem } from '../pos-cart.service';

@Component({
  standalone: true,
  selector: 'app-pos-home',
  imports: [CommonModule, FormsModule],
  templateUrl: './pos-home.component.html',
  styleUrls: ['./pos-home.component.css']
})
export class PosHomeComponent implements OnInit {
  search = '';
  carrito: PosCartItem[] = [];
  productos: any[] = [];
  loading = false;

  constructor(
    private router: Router,
    private productoService: ProductoService,
    private authService: AuthService,
    private cartService: PosCartService
  ) {}

  ngOnInit() {
    this.loadProductos();
    this.carrito = this.cartService.getItems();
  }

  loadProductos() {
    this.loading = true;
    this.productoService.getAll().subscribe({
      next: (productos) => {
        this.productos = (productos || []).map((p: any) => ({
          id: p.id,
          nombre: p.nombre || p.name,
          sku: p.sku,
          precio: p.precio ?? p.sale_price ?? 0,
          stock: p.stock ?? p.quantity ?? p.cantidad ?? p.inventory?.[0]?.quantity ?? 0
        }));
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  get productosFiltrados() {
    const term = this.search.trim().toLowerCase();
    if (!term) return this.productos;
    return this.productos.filter((p: any) =>
      p.nombre?.toLowerCase().includes(term) ||
      p.sku?.toLowerCase().includes(term)
    );
  }

  agregar(producto: any) {
    if (producto.stock <= 0) return;
    this.cartService.upsert({
      id: String(producto.id),
      nombre: producto.nombre,
      precio: producto.precio,
      stock: producto.stock
    });
    this.carrito = this.cartService.getItems();
  }

  sumar(item: any) {
    this.cartService.updateQuantity(item.id, Math.min(item.cantidad + 1, item.stock));
    this.carrito = this.cartService.getItems();
  }

  restar(item: any) {
    this.cartService.updateQuantity(item.id, Math.max(1, item.cantidad - 1));
    this.carrito = this.cartService.getItems();
  }

  eliminar(item: any) {
    this.cartService.remove(item.id);
    this.carrito = this.cartService.getItems();
  }

  total() {
    return this.cartService.total();
  }

  irAPago() {
    this.cartService.setItems(this.carrito);
    this.router.navigate(['/pos/pago'], {
      state: { carrito: this.carrito }
    });
  }

  goDashboard(): void {
    const role = this.authService.getRole();
    const target = this.mapRoleToRoute(role);
    this.router.navigate(['/dashboard', target]);
  }

  goCaja(): void {
    this.router.navigate(['/caja']);
  }

  private mapRoleToRoute(role: string | null): string {
    switch (role) {
      case 'ADMIN': return 'admin';
      case 'CAJERO': return 'cajero';
      case 'ALMACEN': return 'almacen';
      case 'CONTADOR': return 'contador';
      default: return 'admin';
    }
  }
}
