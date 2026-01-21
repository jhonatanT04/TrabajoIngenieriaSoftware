import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { UsuariosService } from '../../../core/services/usuarios.service';
import { Profile } from '../../../core/models/usuario.model';

@Component({
  standalone: true,
  selector: 'app-usuario-create',
  imports: [CommonModule, FormsModule],
  templateUrl: './usuario-create.component.html',
  styleUrls: ['./usuario-create.component.css']
})
export class UsuarioCreateComponent implements OnInit {

  usuario: any = {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    profile_name: 'Cajero',
    is_active: true
  };
  profiles: Profile[] = [];
  selectedProfileId: string | null = null;
  loading = false;
  error = '';

  constructor(
    private service: UsuariosService,
    private router: Router
  ) {}

  ngOnInit() {
    this.service.getProfiles().subscribe({
      next: (profiles) => {
        this.profiles = profiles;
        if (profiles.length > 0) {
          this.selectedProfileId = profiles[0].id;
          this.usuario.profile_name = profiles[0].name;
        }
      },
      error: (err) => {
        console.error('Error cargando perfiles:', err);
        this.profiles = [
          { id: '1', name: 'Administrador', is_active: true },
          { id: '2', name: 'Cajero', is_active: true },
          { id: '3', name: 'Almacen', is_active: true },
          { id: '4', name: 'Contador', is_active: true }
        ];
        this.selectedProfileId = this.profiles[0].id;
        this.usuario.profile_name = this.profiles[0].name;
      }
    });
  }

  guardar() {
    this.loading = true;
    this.error = '';
    const selectedProfile = this.profiles.find(p => p.id === this.selectedProfileId);
    const payload = {
      username: this.usuario.username,
      email: this.usuario.email,
      first_name: this.usuario.first_name,
      last_name: this.usuario.last_name,
      password: this.usuario.password,
      profile_name: selectedProfile?.name || this.usuario.profile_name,
      is_active: this.usuario.is_active
    };

    this.service.create(payload).subscribe({
      next: () => {
        this.router.navigate(['/admin/usuarios']);
      },
      error: (err) => {
        console.error('Error creando usuario:', err);
        this.error = 'Error al crear el usuario. Verifique los datos.';
        this.loading = false;
      }
    });
  }
}
