import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Proveedor {
  id: number;
  nombre: string;
  email: string;
  telefono: string;
  direccion: string;
  ciudad: string;
  contacto: string;
  activo: boolean;
  fechaCreacion: Date;
}

@Component({
  selector: 'app-proveedor-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './proveedor-list.component.html',
  styleUrls: ['./proveedor-list.component.css']
})
export class ProveedorListComponent {

  proveedores: Proveedor[] = [
    {
      id: 1,
      nombre: 'Distribuidora Central',
      email: 'info@distcentral.com',
      telefono: '555-1234',
      direccion: 'Calle Principal 123',
      ciudad: 'Ciudad Principal',
      contacto: 'Juan Rodríguez',
      activo: true,
      fechaCreacion: new Date('2024-01-15')
    },
    {
      id: 2,
      nombre: 'Proveedores Unidos',
      email: 'contacto@proveedores.com',
      telefono: '555-5678',
      direccion: 'Avenida Comercial 456',
      ciudad: 'Centro',
      contacto: 'María García',
      activo: true,
      fechaCreacion: new Date('2024-02-20')
    }
  ];

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredProveedores(): Proveedor[] {
    return this.proveedores.filter(p =>
      p.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      p.email.toLowerCase().includes(this.searchTerm.toLowerCase())
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
    if (confirm(`¿Está seguro de eliminar al proveedor ${proveedor.nombre}?`)) {
      this.proveedores = this.proveedores.filter(p => p.id !== proveedor.id);
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) this.currentPage--;
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) this.currentPage++;
  }
}
