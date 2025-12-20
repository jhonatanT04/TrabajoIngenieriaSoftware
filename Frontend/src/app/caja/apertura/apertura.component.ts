import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Apertura {
  id: number;
  fecha: Date;
  montoInicial: number;
  montoFinal: number;
  estado: string;
}

@Component({
  standalone: true,
  selector: 'app-apertura',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './apertura.component.html',
  styleUrls: ['./apertura.component.css']
})
export class AperturaComponent {

  aperturas: Apertura[] = [
    {
      id: 1,
      fecha: new Date('2024-12-15'),
      montoInicial: 1000.00,
      montoFinal: 1500.50,
      estado: 'Cerrada'
    },
    {
      id: 2,
      fecha: new Date('2024-12-16'),
      montoInicial: 1500.50,
      montoFinal: 2000.00,
      estado: 'Cerrada'
    },
    {
      id: 3,
      fecha: new Date('2024-12-17'),
      montoInicial: 2000.00,
      montoFinal: 0,
      estado: 'Abierta'
    }
  ];

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredAperturas(): Apertura[] {
    return this.aperturas.filter(a =>
      a.estado.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      a.fecha.toString().includes(this.searchTerm)
    );
  }

  get paginatedAperturas(): Apertura[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredAperturas.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredAperturas.length / this.itemsPerPage);
  }

  deleteApertura(apertura: Apertura): void {
    if (confirm(`¿Está seguro de eliminar esta apertura?`)) {
      this.aperturas = this.aperturas.filter(a => a.id !== apertura.id);
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
