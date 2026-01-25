import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-pos-layout',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './pos-layout.component.html',
  styleUrls: ['./pos-layout.component.css']
})
export class PosLayoutComponent {
  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  goToDashboard(): void {
    const role = this.authService.getRole();
    const target = this.mapRoleToRoute(role);
    this.router.navigate(['/dashboard', target]);
  }

  goToCaja(): void {
    this.router.navigate(['/caja']);
  }

  goHome(): void {
    this.router.navigate(['/']);
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
