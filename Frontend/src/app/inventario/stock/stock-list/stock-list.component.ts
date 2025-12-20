import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Stock {
  id: number;
  codigo: string;
  nombre: string;
  categoria: string;
  stockActual: number;
  stockMinimo: number;
  stockMaximo: number;
  ubicacion: string;
  ultimaActualizacion: Date;
}

@Component({
  standalone: true,
  selector: 'app-stock-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './stock-list.component.html',
  styleUrls: ['./stock-list.component.css']
})
export class StockListComponent {

  stocks: Stock[] = [
    {
      id: 1,
      codigo: 'PROD001',
      nombre: 'Arroz Blanco 1kg',
      categoria: 'Alimentos',
      stockActual: 150,
      stockMinimo: 50,
      stockMaximo: 300,
      ubicacion: 'Pasillo A - Estante 3',
      ultimaActualizacion: new Date('2024-12-15')
    },
    {
      id: 2,
      codigo: 'PROD002',
      nombre: 'Leche Integral 1L',
      categoria: 'Lácteos',
      stockActual: 30,
      stockMinimo: 50,
      stockMaximo: 200,
      ubicacion: 'Pasillo B - Refrigerador 1',
      ultimaActualizacion: new Date('2024-12-16')
    },
    {
      id: 3,
      codigo: 'PROD003',
      nombre: 'Pan Integral 500g',
      categoria: 'Panadería',
      stockActual: 80,
      stockMinimo: 40,
      stockMaximo: 150,
      ubicacion: 'Pasillo C - Estante 1',
      ultimaActualizacion: new Date('2024-12-17')
    }
  ];

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredStocks(): Stock[] {
    return this.stocks.filter(s =>
      s.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      s.codigo.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      s.categoria.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  get paginatedStocks(): Stock[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredStocks.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredStocks.length / this.itemsPerPage);
  }

  getStockStatus(stock: Stock): string {
    if (stock.stockActual <= stock.stockMinimo) return 'bajo';
    if (stock.stockActual >= stock.stockMaximo) return 'alto';
    return 'normal';
  }

  getStockBadge(stock: Stock): string {
    const status = this.getStockStatus(stock);
    if (status === 'bajo') return 'badge-danger';
    if (status === 'alto') return 'badge-warning';
    return 'badge-success';
  }

  previousPage(): void {
    if (this.currentPage > 1) this.currentPage--;
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) this.currentPage++;
  }
}
