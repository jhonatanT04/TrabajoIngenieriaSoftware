import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { PosProducto } from '../../core/models/pos-product.model';
import { VentaService } from '../../core/services/venta.service';
import { PosCartItem, PosCartService } from '../pos-cart.service';
import { ClienteService } from '../../core/services/cliente.service';
import { Cliente } from '../../core/models';

@Component({
  standalone: true,
  selector: 'app-pos-pago',
  imports: [CommonModule, FormsModule],
  templateUrl: './pos-pago.component.html',
  styleUrls: ['./pos-pago.component.css']
})
export class PosPagoComponent implements OnInit {
  carrito: (PosProducto | PosCartItem)[] = [];
  efectivo: number = 0;
  loading = false;
  clientes: Cliente[] = [];
  searchCliente = '';
  selectedClienteId: string | null = null;

  constructor(
    private router: Router,
    private ventaService: VentaService,
    private cartService: PosCartService,
    private clienteService: ClienteService
  ) {
    this.carrito = (history.state && history.state.carrito) || this.cartService.getItems();
    if (!this.carrito || this.carrito.length === 0) {
      this.router.navigate(['/pos']);
    }
  }

  ngOnInit(): void {
    this.loadClientes();
  }

  get clientesFiltrados(): Cliente[] {
    const term = this.searchCliente.trim().toLowerCase();
    if (!term) return this.clientes;
    return this.clientes.filter(c =>
      `${c.first_name || ''} ${c.last_name || ''}`.toLowerCase().includes(term) ||
      (c.document_number || '').toLowerCase().includes(term)
    );
  }

  private loadClientes(): void {
    this.clienteService.getAll({ limit: 200 }).subscribe({
      next: (clientes) => {
        this.clientes = clientes || [];
      },
      error: () => {
        this.clientes = [];
      }
    });
  }

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
    this.loading = true;

    const payload = {
      items: this.carrito.map(item => ({
        product_id: String((item as any).id),
        quantity: item.cantidad,
        unit_price: item.precio,
        discount_percentage: 0,
        tax_rate: (item as any).tax_rate ?? 0
      })),
      customer_id: this.selectedClienteId || undefined,
      notes: 'Venta rápida POS'
    } as any;

    this.ventaService.create(payload).subscribe({
      next: (venta) => {
        this.cartService.clear();
        this.loading = false;
        this.router.navigate(['/pos/ticket'], {
          state: {
            carrito: this.carrito,
            total: totalVenta,
            efectivo: this.efectivo,
            vuelto: this.vuelto(),
            venta
          }
        });
      },
      error: (err) => {
        console.error('Error al procesar venta POS', err);
        alert(err?.error?.detail || 'No se pudo procesar la venta');
        this.loading = false;
      }
    });
  }

  cancelar(): void {
    this.router.navigate(['/pos']);
  }
}
