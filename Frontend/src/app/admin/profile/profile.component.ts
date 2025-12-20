import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  standalone: true,
  selector: 'app-profile',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  basePrefix = this.router.url.includes('/pos') ? '/pos' : '/admin';
  changePasswordLink = this.basePrefix === '/pos' ? '/pos/cambiar-password' : '/admin/cambiar-contraseña';
  role = (this.authService.getUser()?.role || '').toUpperCase();
  roleClass = this.role === 'ADMIN' ? 'profile--admin' : 'profile--cajero';

  user = {
    username: this.authService.getUser()?.username || '',
    role: this.role || '',
    email: 'usuario@ejemplo.com',
    nombre: 'Nombre Completo',
    telefono: ''
  };

  editMode = false;

  get isAdmin(): boolean {
    return this.role === 'ADMIN';
  }

  get isCajero(): boolean {
    return this.role === 'CAJERO';
  }

  toggleEdit(): void {
    this.editMode = !this.editMode;
  }

  guardar(): void {
    alert('Perfil actualizado (demo)');
    this.editMode = false;
  }

  cancelar(): void {
    this.editMode = false;
  }

  volver(): void {
    if (this.basePrefix === '/pos') {
      this.router.navigate(['/pos']);
    } else {
      this.router.navigate(['/admin/profile']);
    }
  }
}
