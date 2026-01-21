import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { InventarioService, InventoryMovement } from '../../../core/services/inventario.service';
import { ProductoService } from '../../../core/services/producto.service';
import { Producto } from '../../../core/models/producto.model';

@Component({
  standalone: true,
  selector: 'app-movimiento-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './movimiento-list.component.html',
  styleUrls: ['./movimiento-list.component.css']
})
export class MovimientoListComponent implements OnInit {

  movimientos: InventoryMovement[] = [];
  productos: Producto[] = [];
  loading = true;
  error = '';
  productoFilter = '';

  constructor(
    private inventarioService: InventarioService,
    private productoService: ProductoService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    // Cargar productos para el dropdown
    this.productoService.getAll().subscribe({
      next: (productos) => {
        this.productos = productos;
      },
      error: (err) => {
        console.error('Error cargando productos:', err);
      }
    });

    // Obtener filtro de producto de la URL si existe
    this.route.queryParams.subscribe(params => {
      this.productoFilter = params['producto'] || '';
      this.loadMovimientos();
    });
  }

  private mapMovement(m: InventoryMovement): InventoryMovement {
    return {
      ...m,
      fecha: (m as any).fecha || m.created_at,
      tipo: (m as any).tipo || (m as any).movement_type,
      producto: (m as any).producto || (m as any).product_name || (m as any).product_id,
      cantidad: (m as any).cantidad ?? m.quantity,
      usuario: (m as any).usuario || (m as any).user_name || (m as any).user_id,
    };
  }

  loadMovimientos(): void {
    this.loading = true;
    const params: any = {};
    
    // Si hay filtro de producto, usarlo
    if (this.productoFilter && this.productoFilter.trim()) {
      params.product_id = this.productoFilter.trim();
      console.log('Filtrando por producto:', params.product_id);
    }
    
    this.inventarioService.getMovements(params).subscribe({
      next: (movimientos) => {
        console.log('Movimientos recibidos:', movimientos.length);
        this.movimientos = movimientos.map((m) => this.mapMovement(m));
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando movimientos:', err);
        this.error = 'Error al cargar los movimientos';
        this.loading = false;
      }
    });
  }

  onFilterChange(): void {
    this.currentPage = 1;
    this.loadMovimientos();
  }

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredMovimientos(): InventoryMovement[] {
    return this.movimientos.filter(m => {
      const producto = m.producto || '';
      const tipo = m.tipo || '';
      const usuario = m.usuario || '';
      return producto.toString().toLowerCase().includes(this.searchTerm.toLowerCase()) ||
             tipo.toString().toLowerCase().includes(this.searchTerm.toLowerCase()) ||
             usuario.toString().toLowerCase().includes(this.searchTerm.toLowerCase());
    });
  }

  get paginatedMovimientos(): InventoryMovement[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredMovimientos.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredMovimientos.length / this.itemsPerPage);
  }

  deleteMovimiento(movimiento: InventoryMovement): void {
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
