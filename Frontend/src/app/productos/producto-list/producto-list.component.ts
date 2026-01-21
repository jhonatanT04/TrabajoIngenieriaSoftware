import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProductoService } from '../../core/services/producto.service';
import { Producto } from '../../core/models/producto.model';

@Component({
  selector: 'app-producto-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './producto-list.component.html',
  styleUrls: ['./producto-list.component.css']
})
export class ProductoListComponent implements OnInit {

  productos: Producto[] = [];
  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;
  loading = true;
  error = '';

  constructor(private productoService: ProductoService) {}

  ngOnInit(): void {
    this.loadProductos();
  }

  loadProductos(): void {
    this.loading = true;
    this.productoService.getAll().subscribe({
      next: (productos) => {
        this.productos = productos;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando productos:', err);
        this.error = 'Error al cargar productos';
        this.loading = false;
      }
    });
  }

  get filteredProductos(): Producto[] {
    if (!this.searchTerm) return this.productos;
    return this.productos.filter(p =>
      p.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      p.sku.toLowerCase().includes(this.searchTerm.toLowerCase())
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
    if (confirm(`¿Está seguro de eliminar el producto ${producto.name}?`)) {
      this.productoService.delete(producto.id!).subscribe({
        next: () => {
          this.loadProductos();
        },
        error: (err) => {
          console.error('Error eliminando producto:', err);
          alert('Error al eliminar el producto');
        }
      });
    }
  }

  toggleStatus(producto: Producto): void {
    const nuevoEstado = !producto.is_active;
    this.productoService.update(producto.id!, { is_active: nuevoEstado }).subscribe({
      next: () => {
        producto.is_active = nuevoEstado;
      },
      error: (err) => {
        console.error('Error actualizando estado:', err);
        alert('Error al actualizar el estado del producto');
      }
    });
  }

  previousPage(): void {
    if (this.currentPage > 1) this.currentPage--;
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) this.currentPage++;
  }
}
