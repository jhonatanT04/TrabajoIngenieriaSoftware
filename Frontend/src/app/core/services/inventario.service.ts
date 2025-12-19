import { Injectable } from '@angular/core';

export interface Producto {
  id: number;
  nombre: string;
  precio: number;
  stock: number;
}

@Injectable({ providedIn: 'root' })
export class InventarioService {

  productos: Producto[] = [
    { id: 1, nombre: 'Arroz', precio: 1.25, stock: 50 },
    { id: 2, nombre: 'Azúcar', precio: 1.10, stock: 30 },
    { id: 3, nombre: 'Leche', precio: 0.95, stock: 20 }
  ];

  getProductos() {
    return this.productos;
  }

  getById(id: number) {
    return this.productos.find(p => p.id === id);
  }

  descontarStock(id: number, cantidad: number) {
    const producto = this.getById(id);
    if (producto) {
      producto.stock -= cantidad;
    }
  }

  ajustarStock(id: number, cantidad: number) {
    const producto = this.getById(id);
    if (producto) {
      producto.stock += cantidad;
    }
  }
}
