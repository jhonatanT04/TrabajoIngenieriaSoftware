import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProveedorService } from '../../core/services/proveedor.service';
import { Proveedor } from '../../core/models/producto.model';

@Component({
  selector: 'app-proveedor-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './proveedor-list.component.html',
  styleUrls: ['./proveedor-list.component.css']
})
export class ProveedorListComponent implements OnInit {

  proveedores: Proveedor[] = [];
  loading = true;
  error = '';
  searchTerm = '';

  constructor(private proveedorService: ProveedorService) {}

  ngOnInit(): void {
    this.loadProveedores();
  }

  loadProveedores(): void {
    this.loading = true;
    this.proveedorService.getAll().subscribe({
      next: (proveedores) => {
        this.proveedores = proveedores;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando proveedores:', err);
        this.error = 'Error al cargar proveedores';
        this.loading = false;
      }
    });
  }

  currentPage = 1;
  itemsPerPage = 10;

  get filteredProveedores(): Proveedor[] {
    if (!this.searchTerm) return this.proveedores;
    return this.proveedores.filter(p =>
      p.business_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      (p.email && p.email.toLowerCase().includes(this.searchTerm.toLowerCase()))
    );
  }

  get paginatedProveedores(): Proveedor[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredProveedores.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredProveedores.length / this.itemsPerPage);
  }

  deleteProveedor(proveedor: Proveedor): void {
    if (confirm(`¿Está seguro de eliminar al proveedor ${proveedor.business_name}?`)) {
      this.proveedorService.delete(proveedor.id).subscribe({
        next: () => {
          this.loadProveedores();
        },
        error: (err) => {
          console.error('Error eliminando proveedor:', err);
          alert('Error al eliminar el proveedor');
        }
      });
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) this.currentPage--;
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) this.currentPage++;
  }
}
