import { Component, inject } from '@angular/core';
import { Router, RouterOutlet, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-pos-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  templateUrl: './pos-layout.component.html',
  styleUrls: ['./pos-layout.component.css']
})
export class PosLayoutComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  user = this.authService.getUser();

  logout() {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }

  goDashboard(): void {
    const role = this.authService.getRole();
    const target = this.mapRoleToRoute(role);
    this.router.navigate(['/dashboard', target]);
  }

  goCaja(): void {
    this.router.navigate(['/caja']);
  }

  private mapRoleToRoute(role: string | null): string {
    switch (role) {
      case 'ADMIN': return 'admin';
      case 'CAJERO': return 'cajero';
      case 'ALMACEN': return 'almacen';
      case 'CONTADOR': return 'contador';
      default: return 'admin';
    }
  }
}
