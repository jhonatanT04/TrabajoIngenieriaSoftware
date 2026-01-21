import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { VentaService } from '../../core/services/venta.service';
import { DialogService } from '../../shared/services/dialog.service';
import { Venta } from '../../core/models';

interface VentaDisplay {
  id: string;
  created_at: Date;
  customer_name: string;
  total: number;
  status: string;
  user_name: string;
  [key: string]: any;
}

@Component({
  standalone: true,
  selector: 'app-venta-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './venta-list.component.html',
  styleUrls: ['./venta-list.component.css']
})
export class VentaListComponent implements OnInit {

  ventas: VentaDisplay[] = [];
  loading = true;
  error = '';

  constructor(
    private ventaService: VentaService,
    private dialogService: DialogService
  ) {}

  ngOnInit(): void {
    this.loadVentas();
  }

  loadVentas(): void {
    this.loading = true;
    this.ventaService.getAll().subscribe({
      next: (data: any) => {
        // Transformar datos del backend al formato esperado por el template
        this.ventas = (Array.isArray(data) ? data : []).map((v: any) => ({
          id: v.id,
          created_at: new Date(v.created_at || v.sale_date),
          customer_name: v.customer 
            ? `${v.customer.first_name} ${v.customer.last_name}`
            : 'Cliente General',
          total: v.total_amount || v.total,
          status: v.status || 'PENDING',
          user_name: v.cashier 
            ? `${v.cashier.first_name} ${v.cashier.last_name}`
            : (v.cashier?.username || 'Sin vendedor'),
          ...v
        }));
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando ventas:', err);
        this.error = 'Error al cargar las ventas';
        this.loading = false;
      }
    });
  }

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredVentas(): VentaDisplay[] {
    return this.ventas.filter(v =>
      v.customer_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      v.user_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      v.status.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  get paginatedVentas(): VentaDisplay[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredVentas.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredVentas.length / this.itemsPerPage);
  }

  deleteVenta(venta: VentaDisplay): void {
    console.log('🗑️ Intentando eliminar venta:', venta);
    this.dialogService.confirm({
      title: 'Eliminar Venta',
      message: `¿Está seguro de que desea eliminar la venta ${venta['sale_number']}?`,
      confirmText: 'Eliminar',
      cancelText: 'Cancelar'
    }).then(confirmed => {
      if (confirmed) {
        console.log('✅ Usuario confirmó eliminación, llamando al servicio...');
        // Llamar al servicio para eliminar del backend
        this.ventaService.delete(venta.id).subscribe({
          next: () => {
            console.log('✅ Venta eliminada del servidor');
            // Remover de la lista local
            this.ventas = this.ventas.filter(v => v.id !== venta.id);
            if (this.currentPage > this.totalPages && this.totalPages > 0) {
              this.currentPage = this.totalPages;
            }
            this.error = '';
          },
          error: (err) => {
            console.error('❌ Error al eliminar venta:', err);
            this.error = 'Error al eliminar la venta: ' + (err.error?.detail || err.message || 'Error desconocido');
          }
        });
      } else {
        console.log('❌ Usuario canceló la eliminación');
      }
    });
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
