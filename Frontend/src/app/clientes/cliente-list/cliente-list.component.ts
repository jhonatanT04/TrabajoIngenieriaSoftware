import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ClienteService } from '../../core/services/cliente.service';
import { Cliente } from '../../core/models/venta.model';

@Component({
  standalone: true,
  selector: 'app-cliente-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './cliente-list.component.html',
  styleUrls: ['./cliente-list.component.css']
})
export class ClienteListComponent implements OnInit {

  clientes: Cliente[] = [];
  loading = true;
  error = '';
  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  constructor(private clienteService: ClienteService) {}

  ngOnInit(): void {
    this.loadClientes();
  }

  loadClientes(): void {
    this.loading = true;
    this.clienteService.getAll().subscribe({
      next: (clientes) => {
        this.clientes = clientes;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando clientes:', err);
        this.error = 'Error al cargar clientes';
        this.loading = false;
      }
    });
  }

  get filteredClientes(): Cliente[] {
    if (!this.searchTerm) return this.clientes;
    return this.clientes.filter(c =>
      c.first_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      c.last_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      (c.email && c.email.toLowerCase().includes(this.searchTerm.toLowerCase())) ||
      (c.phone && c.phone.includes(this.searchTerm)) ||
      (c.document_number && c.document_number.includes(this.searchTerm))
    );
  }

  get paginatedClientes(): Cliente[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredClientes.slice(start, start + this.itemsPerPage);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredClientes.length / this.itemsPerPage);
  }

  deleteCliente(cliente: Cliente): void {
    if (confirm(`¿Está seguro de eliminar a ${cliente.first_name} ${cliente.last_name}?`)) {
      this.clienteService.delete(cliente.id).subscribe({
        next: () => {
          this.loadClientes();
        },
        error: (err) => {
          console.error('Error eliminando cliente:', err);
          alert('Error al eliminar el cliente');
        }
      });
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
