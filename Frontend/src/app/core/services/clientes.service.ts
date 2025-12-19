import { Injectable } from '@angular/core';

export interface Cliente {
  id: number;
  nombre: string;
  cedula: string;
  email: string;
  puntos: number;
}

@Injectable({ providedIn: 'root' })
export class ClientesService {

  private clientes: Cliente[] = [
    { id: 1, nombre: 'Juan Pérez', cedula: '0102030405', email: 'juan@mail.com', puntos: 120 }
  ];

  getAll() {
    return this.clientes;
  }

  getById(id: number) {
    return this.clientes.find(c => c.id === id);
  }

  create(cliente: Cliente) {
    cliente.id = Date.now();
    cliente.puntos = 0;
    this.clientes.push(cliente);
  }

  update(cliente: Cliente) {
    const i = this.clientes.findIndex(c => c.id === cliente.id);
    this.clientes[i] = cliente;
  }
}
