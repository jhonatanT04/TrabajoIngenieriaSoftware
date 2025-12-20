import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Reporte {
  id: number;
  nombre: string;
  tipo: string;
  fechaCreacion: Date;
  acciones: string;
}

@Component({
  standalone: true,
  selector: 'app-reportes-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './reportes-list.component.html',
  styleUrls: ['./reportes-list.component.css']
})
export class ReportesListComponent {

  reportes: Reporte[] = [
    {
      id: 1,
      nombre: 'Reporte de Ventas Diario',
      tipo: 'Ventas',
      fechaCreacion: new Date('2024-12-15'),
      acciones: 'Descargar/Ver'
    },
    {
      id: 2,
      nombre: 'Reporte de Inventario',
      tipo: 'Inventario',
      fechaCreacion: new Date('2024-12-16'),
      acciones: 'Descargar/Ver'
    },
    {
      id: 3,
      nombre: 'Reporte de Clientes',
      tipo: 'Clientes',
      fechaCreacion: new Date('2024-12-17'),
      acciones: 'Descargar/Ver'
    }
  ];

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredReportes(): Reporte[] {
    return this.reportes.filter(r =>
      r.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      r.tipo.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  get paginatedReportes(): Reporte[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredReportes.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredReportes.length / this.itemsPerPage);
  }

  deleteReporte(reporte: Reporte): void {
    if (confirm(`¿Está seguro de eliminar el reporte ${reporte.nombre}?`)) {
      this.reportes = this.reportes.filter(r => r.id !== reporte.id);
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
