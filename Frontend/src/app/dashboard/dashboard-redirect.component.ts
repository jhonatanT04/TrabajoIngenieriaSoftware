import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../core/services/auth.service';

@Component({
  standalone: true,
  selector: 'app-dashboard-redirect',
  imports: [CommonModule],
  template: `
    <div class="redirect-wrapper">
      <div class="redirect-card">
        <span class="material-icons">autorenew</span>
        <div class="redirect-text">Redirigiendo a tu panel...</div>
      </div>
    </div>
  `,
  styles: [`
    .redirect-wrapper { display: grid; place-items: center; height: 60vh; color: #2f3b52; }
    .redirect-card { display: flex; gap: 0.75rem; align-items: center; padding: 1rem 1.25rem; background: #f5f7fb; border-radius: 12px; box-shadow: 0 6px 24px rgba(47, 59, 82, 0.08); }
    .redirect-card .material-icons { font-size: 28px; animation: spin 1.2s linear infinite; }
    .redirect-text { font-weight: 600; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
  `]
})
export class DashboardRedirectComponent implements OnInit {
  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const role = this.authService.getRole();
    const target = this.mapRoleToRoute(role);
    this.router.navigate(['/dashboard', target], { replaceUrl: true });
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
