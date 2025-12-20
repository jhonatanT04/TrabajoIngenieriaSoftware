import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-change-password',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css']
})
export class ChangePasswordComponent {

  passwordData = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  };

  showCurrentPassword = false;
  showNewPassword = false;
  showConfirmPassword = false;

  constructor(private router: Router) {}

  cambiarPassword(): void {
    if (this.passwordData.newPassword !== this.passwordData.confirmPassword) {
      alert('Las contraseñas no coinciden');
      return;
    }

    if (this.passwordData.newPassword.length < 6) {
      alert('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    alert('Contraseña cambiada exitosamente');
    this.volver();
  }

  cancelar(): void {
    this.volver();
  }

  volver(): void {

    const currentUrl = this.router.url;
    if (currentUrl.includes('/pos/')) {
      this.router.navigate(['/pos/profile']);
    } else {
      this.router.navigate(['/admin/profile']);
    }
  }
}
