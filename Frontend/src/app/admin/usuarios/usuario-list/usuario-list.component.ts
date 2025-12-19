import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { UsuariosService, Usuario } from '../../../core/services/usuarios.service';

@Component({
  standalone: true,
  selector: 'app-usuario-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './usuario-list.component.html'
})
export class UsuarioListComponent {

  // ✅ Declaramos la propiedad explícitamente con tipo
  public usuarios: Usuario[] = [];

  constructor(private service: UsuariosService) {
    // ✅ Inicializamos la propiedad
    this.usuarios = this.service.getAll();
  }
}
