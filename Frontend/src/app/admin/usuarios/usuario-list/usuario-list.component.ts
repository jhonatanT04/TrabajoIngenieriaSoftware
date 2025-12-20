import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { UsuariosService } from '../../../core/services/usuarios.service';
import { Usuario } from '../../../core/models/usuario.model';

@Component({
  standalone: true,
  selector: 'app-usuario-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './usuario-list.component.html',
  styleUrls: ['./usuario-list.component.css']
})
export class UsuarioListComponent {

  public usuarios: Usuario[] = [];

  constructor(private service: UsuariosService) {
    this.usuarios = this.service.getAll();
  }

  getRoleBadgeClass(role: string): string {
    const roleClasses: { [key: string]: string } = {
      'ADMIN': 'badge-danger',
      'CAJERO': 'badge-info',
      'ALMACEN': 'badge-warning',
      'CONTADOR': 'badge-success'
    };
    return roleClasses[role] || 'badge-primary';
  }

  deleteUsuario(usuario: Usuario): void {
    if (confirm(`¿Estás seguro de eliminar al usuario ${usuario.nombre} ${usuario.apellido}?`)) {
      // Aquí conectarás con el backend
      console.log('Eliminar usuario:', usuario.id);
    }
  }
}
