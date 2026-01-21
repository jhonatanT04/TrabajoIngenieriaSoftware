import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { UsuariosService } from '../../../core/services/usuarios.service';
import { Usuario, Profile } from '../../../core/models/usuario.model';

@Component({
  standalone: true,
  selector: 'app-usuario-edit',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './usuario-edit.component.html'
})
export class UsuarioEditComponent implements OnInit {

  usuario?: Usuario;
  profiles: Profile[] = [];
  selectedProfileId: string | null = null;
  newPassword: string = '';
  loading = true;
  saving = false;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private service: UsuariosService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id')!;
    
    this.service.getById(id).subscribe({
      next: (usuario) => {
        this.usuario = { ...usuario };
        this.selectedProfileId = usuario.profile?.id || usuario.profile_id;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando usuario:', err);
        this.error = 'Error al cargar el usuario';
        this.loading = false;
      }
    });

    this.service.getProfiles().subscribe({
      next: (profiles) => {
        this.profiles = profiles;
      },
      error: (err) => {
        console.error('Error cargando perfiles:', err);
        this.profiles = [
          { id: '1', name: 'Administrador', is_active: true },
          { id: '2', name: 'Cajero', is_active: true },
          { id: '3', name: 'Almacen', is_active: true },
          { id: '4', name: 'Contador', is_active: true }
        ];
      }
    });
  }

  guardar() {
    if (!this.usuario) return;
    
    this.saving = true;
    this.error = '';
    const selectedProfile = this.profiles.find(p => p.id === this.selectedProfileId);
    const payload: any = {
      username: this.usuario.username,
      email: this.usuario.email,
      first_name: this.usuario.first_name,
      last_name: this.usuario.last_name,
      is_active: this.usuario.is_active,
      profile_name: selectedProfile?.name || this.usuario.profile?.name
    };

    if (this.newPassword) {
      payload.password = this.newPassword;
    }

    this.service.update(this.usuario.id, payload).subscribe({
      next: () => {
        this.router.navigate(['/admin/usuarios']);
      },
      error: (err) => {
        console.error('Error actualizando usuario:', err);
        this.error = 'Error al actualizar el usuario';
        this.saving = false;
      }
    });
  }
}
