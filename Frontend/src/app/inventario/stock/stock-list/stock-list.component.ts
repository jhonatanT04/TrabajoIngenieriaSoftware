import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProductoService } from '../../../core/services/producto.service';
import { InventarioService, InventoryItem } from '../../../core/services/inventario.service';
import { Producto } from '../../../core/models/producto.model';
import { forkJoin } from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-stock-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './stock-list.component.html',
  styleUrls: ['./stock-list.component.css']
})
export class StockListComponent implements OnInit {

  productos: Producto[] = [];
  inventarios: InventoryItem[] = [];
  loading = true;
  error = '';

  constructor(
    private productoService: ProductoService,
    private inventarioService: InventarioService
  ) {}

  ngOnInit(): void {
    this.loadStock();
  }

  loadStock(): void {
    this.loading = true;
    // Cargar productos e inventarios en paralelo
    forkJoin({
      productos: this.productoService.getAll(),
      inventarios: this.inventarioService.getAll()
    }).subscribe({
      next: ({ productos, inventarios }) => {
        this.productos = productos;
        this.inventarios = inventarios;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando stock:', err);
        this.error = 'Error al cargar el stock';
        this.loading = false;
      }
    });
  }

  get stocks(): any[] {
    return this.productos.map(p => {
      // Buscar el inventario correspondiente
      const inventario = this.inventarios.find(inv => inv.product_id === p.id);
      
      return {
        id: p.id,
        codigo: p.sku,
        nombre: p.name,
        categoria: (p as any).category?.name || (p as any).categoryName || 'Sin categoría',
        stockActual: inventario?.quantity || 0,
        stockMinimo: (p as any).stock_min || 0,
        stockMaximo: (p as any).stock_max || 0,
        ubicacion: 'Almacén principal',
        ultimaActualizacion: inventario?.last_updated ? new Date(inventario.last_updated) : new Date()
      };
    });
  }

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredStocks(): any[] {
    return this.stocks.filter(s =>
      s.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      s.codigo.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      s.categoria.toString().toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  get paginatedStocks(): any[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredStocks.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredStocks.length / this.itemsPerPage);
  }

  getStockStatus(stock: any): string {
    if (stock.stockActual <= stock.stockMinimo) return 'bajo';
    if (stock.stockActual >= stock.stockMaximo) return 'alto';
    return 'normal';
  }

  getStockBadge(stock: any): string {
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

  verHistorial(productId: string): void {
    // Navegar a movimientos con filtro por producto
    window.location.href = `/inventario/movimientos?producto=${productId}`;
  }
}
