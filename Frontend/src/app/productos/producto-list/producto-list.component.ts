import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Producto {
  id: number;
  codigo: string;
  nombre: string;
  descripcion: string;
  precioCompra: number;
  precioVenta: number;
  stock: number;
  categoria: string;
  proveedor: string;
  activo: boolean;
  fechaCreacion: Date;
}

@Component({
  selector: 'app-producto-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './producto-list.component.html',
  styleUrls: ['./producto-list.component.css']
})
export class ProductoListComponent {

  productos: Producto[] = [
    {
      id: 1,
      codigo: 'PROD001',
      nombre: 'Arroz Blanco 1kg',
      descripcion: 'Arroz de excelente calidad',
      precioCompra: 1.20,
      precioVenta: 2.50,
      stock: 150,
      categoria: 'Alimentos',
      proveedor: 'Proveedor A',
      activo: true,
      fechaCreacion: new Date('2024-01-15')
    },
    {
      id: 2,
      codigo: 'PROD002',
      nombre: 'Leche Integral 1L',
      descripcion: 'Leche fresca pasteurizada',
      precioCompra: 0.80,
      precioVenta: 1.50,
      stock: 200,
      categoria: 'Lácteos',
      proveedor: 'Proveedor B',
      activo: true,
      fechaCreacion: new Date('2024-01-20')
    },
    {
      id: 3,
      codigo: 'PROD003',
      nombre: 'Pan Integral 500g',
      descripcion: 'Pan recién horneado',
      precioCompra: 0.50,
      precioVenta: 1.00,
      stock: 80,
      categoria: 'Panadería',
      proveedor: 'Panadería Local',
      activo: true,
      fechaCreacion: new Date('2024-02-10')
    }
  ];

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredProductos(): Producto[] {
    return this.productos.filter(p =>
      p.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      p.codigo.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  get paginatedProductos(): Producto[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredProductos.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredProductos.length / this.itemsPerPage);
  }

  deleteProducto(producto: Producto): void {
    if (confirm(`¿Está seguro de eliminar el producto ${producto.nombre}?`)) {
      this.productos = this.productos.filter(p => p.id !== producto.id);
    }
  }

  toggleStatus(producto: Producto): void {
    producto.activo = !producto.activo;
  }

  previousPage(): void {
    if (this.currentPage > 1) this.currentPage--;
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) this.currentPage++;
  }
}
