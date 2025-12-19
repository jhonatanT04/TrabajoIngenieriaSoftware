import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { UsuariosService } from '../../../core/services/usuarios.service';

@Component({
  standalone: true,
  selector: 'app-usuario-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './usuario-detail.component.html'
})
export class UsuarioDetailComponent {
  usuario: any;

  constructor(route: ActivatedRoute, service: UsuariosService) {
    this.usuario = service.getById(+route.snapshot.paramMap.get('id')!);
  }
}
