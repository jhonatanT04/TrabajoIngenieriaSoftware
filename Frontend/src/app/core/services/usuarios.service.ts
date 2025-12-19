import { Injectable } from '@angular/core';

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol: string;
}

@Injectable({ providedIn: 'root' })
export class UsuariosService {

  private usuarios: Usuario[] = [
    { id: 1, nombre: 'Administrador', email: 'admin@mail.com', rol: 'ADMIN' },
    { id: 2, nombre: 'Cajero', email: 'caja@mail.com', rol: 'CAJERO' }
  ];

  getAll() {
    return this.usuarios;
  }

  getById(id: number) {
    return this.usuarios.find(u => u.id === id);
  }

  create(usuario: Usuario) {
    usuario.id = Date.now();
    this.usuarios.push(usuario);
  }

  update(usuario: Usuario) {
    const i = this.usuarios.findIndex(u => u.id === usuario.id);
    if (i >= 0) this.usuarios[i] = usuario;
  }
}
