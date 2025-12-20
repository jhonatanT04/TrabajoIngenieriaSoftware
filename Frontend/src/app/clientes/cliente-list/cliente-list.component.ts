import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Cliente {
  id: number;
  nombre: string;
  email: string;
  telefono: string;
  deuda: number;
  estado: string;
}

@Component({
  standalone: true,
  selector: 'app-cliente-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './cliente-list.component.html',
  styleUrls: ['./cliente-list.component.css']
})
export class ClienteListComponent {

  clientes: Cliente[] = [
    {
      id: 1,
      nombre: 'Juan Pérez',
      email: 'juan@example.com',
      telefono: '123456789',
      deuda: 0,
      estado: 'Activo'
    },
    {
      id: 2,
      nombre: 'María García',
      email: 'maria@example.com',
      telefono: '987654321',
      deuda: 250.50,
      estado: 'Activo'
    },
    {
      id: 3,
      nombre: 'Carlos López',
      email: 'carlos@example.com',
      telefono: '555666777',
      deuda: 100.00,
      estado: 'Inactivo'
    }
  ];

  searchTerm = '';
  currentPage = 1;
  itemsPerPage = 10;

  get filteredClientes(): Cliente[] {
    return this.clientes.filter(c =>
      c.nombre.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      c.email.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      c.telefono.includes(this.searchTerm)
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
    if (confirm(`¿Está seguro de eliminar a ${cliente.nombre}?`)) {
      this.clientes = this.clientes.filter(c => c.id !== cliente.id);
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
