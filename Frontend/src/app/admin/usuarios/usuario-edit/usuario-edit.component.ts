import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UsuariosService } from '../../../core/services/usuarios.service';
import { RolesService } from '../../../core/services/roles.service';

@Component({
  standalone: true,
  selector: 'app-usuario-edit',
  imports: [CommonModule, FormsModule],
  templateUrl: './usuario-edit.component.html'
})
export class UsuarioEditComponent {

  usuario: any;
 roles: string[] = [];

  constructor(
    route: ActivatedRoute,
    private service: UsuariosService,
    private rolesService: RolesService,
    private router: Router
  ) {
    this.usuario = { ...this.service.getById(+route.snapshot.paramMap.get('id')!) };
  }

  guardar() {
    this.service.update(this.usuario);
    this.router.navigate(['/admin/usuarios']);
  }
}
