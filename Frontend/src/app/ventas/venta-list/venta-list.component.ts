import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Venta {
  id: number;
  fecha: Date;
  cliente: string;
  monto: number;
  estado: string;
  vendedor: string;
}

@Component({
  standalone: true,
  selector: 'app-venta-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './venta-list.component.html',
  styleUrls: ['./venta-list.component.css']
})
export class VentaListComponent {

  ventas: Venta[] = [
    {
      id: 1,
      fecha: new Date('2024-12-15'),
      cliente: 'Cliente A',
      monto: 150.50,
      estado: 'Completada',
      vendedor: 'Juan Pérez'
    },
    {
      id: 2,
      fecha: new Date('2024-12-16'),
      cliente: 'Cliente B',
      monto: 200.00,
      estado: 'Completada',
      vendedor: 'María García'
    },
    {
      id: 3,
      fecha: new Date('2024-12-17'),
      cliente: 'Cliente C',
      monto: 75.25,
      estado: 'Pendiente',
      vendedor: 'Carlos López'
    }
  ];

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredVentas(): Venta[] {
    return this.ventas.filter(v =>
      v.cliente.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      v.vendedor.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      v.estado.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  get paginatedVentas(): Venta[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredVentas.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredVentas.length / this.itemsPerPage);
  }

  deleteVenta(venta: Venta): void {
    if (confirm(`¿Está seguro de eliminar esta venta?`)) {
      this.ventas = this.ventas.filter(v => v.id !== venta.id);
      if (this.currentPage > this.totalPages && this.totalPages > 0) {
        this.currentPage = this.totalPages;
      }
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }
}
