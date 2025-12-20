import { Injectable } from '@angular/core';
import { Usuario, Rol } from '../models/usuario.model';

@Injectable({ providedIn: 'root' })
export class UsuariosService {

  private roles: Rol[] = [
    {
      id: 1,
      nombre: 'ADMIN',
      descripcion: 'Administrador del sistema',
      permisos: ['all'],
      activo: true
    },
    {
      id: 2,
      nombre: 'CAJERO',
      descripcion: 'Cajero de ventas',
      permisos: ['ventas', 'caja'],
      activo: true
    },
    {
      id: 3,
      nombre: 'ALMACEN',
      descripcion: 'Encargado de almacén',
      permisos: ['inventario', 'productos'],
      activo: true
    },
    {
      id: 4,
      nombre: 'CONTADOR',
      descripcion: 'Contador',
      permisos: ['reportes', 'finanzas'],
      activo: true
    }
  ];

  private usuarios: Usuario[] = [
    {
      id: 1,
      username: 'admin',
      nombre: 'Juan',
      apellido: 'Pérez',
      email: 'admin@mail.com',
      telefono: '555-1234',
      rol: this.roles[0],
      rolId: 1,
      activo: true,
      fechaCreacion: new Date('2024-01-15'),
      ultimoAcceso: new Date('2024-12-19T10:30:00'),
      avatar: ''
    },
    {
      id: 2,
      username: 'cajero1',
      nombre: 'María',
      apellido: 'González',
      email: 'maria@mail.com',
      telefono: '555-5678',
      rol: this.roles[1],
      rolId: 2,
      activo: true,
      fechaCreacion: new Date('2024-03-20'),
      ultimoAcceso: new Date('2024-12-19T09:15:00'),
      avatar: ''
    },
    {
      id: 3,
      username: 'almacen1',
      nombre: 'Carlos',
      apellido: 'Rodríguez',
      email: 'carlos@mail.com',
      telefono: '555-9012',
      rol: this.roles[2],
      rolId: 3,
      activo: true,
      fechaCreacion: new Date('2024-05-10'),
      ultimoAcceso: new Date('2024-12-18T16:45:00'),
      avatar: ''
    },
    {
      id: 4,
      username: 'contador1',
      nombre: 'Ana',
      apellido: 'Martínez',
      email: 'ana@mail.com',
      telefono: '555-3456',
      rol: this.roles[3],
      rolId: 4,
      activo: true,
      fechaCreacion: new Date('2024-06-25'),
      ultimoAcceso: new Date('2024-12-19T08:00:00'),
      avatar: ''
    },
    {
      id: 5,
      username: 'cajero2',
      nombre: 'Luis',
      apellido: 'Hernández',
      email: 'luis@mail.com',
      telefono: '555-7890',
      rol: this.roles[1],
      rolId: 2,
      activo: false,
      fechaCreacion: new Date('2024-08-15'),
      ultimoAcceso: undefined,
      avatar: ''
    }
  ];

  getAll(): Usuario[] {
    return this.usuarios;
  }

  getById(id: number): Usuario | undefined {
    return this.usuarios.find(u => u.id === id);
  }

  create(usuario: Usuario): void {
    usuario.id = Date.now();
    usuario.fechaCreacion = new Date();
    this.usuarios.push(usuario);
  }

  update(usuario: Usuario): void {
    const i = this.usuarios.findIndex(u => u.id === usuario.id);
    if (i >= 0) this.usuarios[i] = usuario;
  }

  delete(id: number): void {
    const i = this.usuarios.findIndex(u => u.id === id);
    if (i >= 0) this.usuarios.splice(i, 1);
  }

  getRoles(): Rol[] {
    return this.roles;
  }
}
