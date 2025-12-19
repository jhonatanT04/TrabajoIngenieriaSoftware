import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { UsuariosService } from '../../../core/services/usuarios.service';
import { RolesService } from '../../../core/services/roles.service';

@Component({
  standalone: true,
  selector: 'app-usuario-create',
  imports: [CommonModule, FormsModule],
  templateUrl: './usuario-create.component.html'
})
export class UsuarioCreateComponent implements OnInit {

  usuario: any = {};
  roles: string[] = [];

  constructor(
    private service: UsuariosService,
    private rolesService: RolesService,
    private router: Router
  ) {}

  ngOnInit() {
    this.roles = this.rolesService.getAll();
  }

  guardar() {
    this.service.create(this.usuario);
    this.router.navigate(['/admin/usuarios']);
  }
}
