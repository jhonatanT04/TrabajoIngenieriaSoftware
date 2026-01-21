import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { UsuariosService } from '../../../core/services/usuarios.service';
import { Usuario } from '../../../core/models/usuario.model';

@Component({
  standalone: true,
  selector: 'app-usuario-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './usuario-detail.component.html'
})
export class UsuarioDetailComponent implements OnInit {
  usuario?: Usuario;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private service: UsuariosService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      this.error = 'ID de usuario no válido';
      this.loading = false;
      return;
    }
    this.service.getById(id).subscribe({
      next: (usuario) => {
        this.usuario = usuario;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando usuario:', err);
        this.error = 'Error al cargar el usuario';
        this.loading = false;
      }
    });
  }
}
