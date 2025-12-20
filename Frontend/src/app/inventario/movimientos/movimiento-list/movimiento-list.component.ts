import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Movimiento {
  id: number;
  fecha: Date;
  tipo: string;
  producto: string;
  cantidad: number;
  usuario: string;
}

@Component({
  standalone: true,
  selector: 'app-movimiento-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './movimiento-list.component.html',
  styleUrls: ['./movimiento-list.component.css']
})
export class MovimientoListComponent {

  movimientos: Movimiento[] = [
    {
      id: 1,
      fecha: new Date('2024-12-15'),
      tipo: 'Entrada',
      producto: 'Arroz Blanco 1kg',
      cantidad: 50,
      usuario: 'Juan Pérez'
    },
    {
      id: 2,
      fecha: new Date('2024-12-16'),
      tipo: 'Salida',
      producto: 'Leche Integral 1L',
      cantidad: 30,
      usuario: 'María García'
    },
    {
      id: 3,
      fecha: new Date('2024-12-17'),
      tipo: 'Ajuste',
      producto: 'Pan Integral 500g',
      cantidad: 5,
      usuario: 'Carlos López'
    }
  ];

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredMovimientos(): Movimiento[] {
    return this.movimientos.filter(m =>
      m.producto.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      m.tipo.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      m.usuario.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  get paginatedMovimientos(): Movimiento[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredMovimientos.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredMovimientos.length / this.itemsPerPage);
  }

  deleteMovimiento(movimiento: Movimiento): void {
    if (confirm(`¿Está seguro de eliminar este movimiento?`)) {
      this.movimientos = this.movimientos.filter(m => m.id !== movimiento.id);
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
