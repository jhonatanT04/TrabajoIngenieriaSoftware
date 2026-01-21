import { Component, computed, inject, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, NavigationEnd } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

interface MenuItem {
  label: string;
  icon?: string;
  route: string;
  roles: string[];
}

@Component({
  selector: 'app-admin-layout',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './admin-layout.component.html',
  styleUrls: ['./admin-layout.component.css']
})
export class AdminLayoutComponent {

  private authService = inject(AuthService);
  private router = inject(Router);

  user = this.authService.getUser();
  showUserMenu = false;

  menu: MenuItem[] = [
    {
      label: 'Dashboard',
      route: '/dashboard',
      roles: ['ADMIN', 'CAJERO', 'ALMACEN', 'CONTADOR']
    },
    {
      label: 'Usuarios',
      route: '/admin/usuarios',
      roles: ['ADMIN']
    },
    {
      label: 'Productos',
      route: '/productos',
      roles: ['ADMIN', 'ALMACEN']
    },
    {
      label: 'Proveedores',
      route: '/proveedores',
      roles: ['ADMIN', 'ALMACEN']
    },
    {
      label: 'Inventario',
      route: '/inventario',
      roles: ['ADMIN', 'ALMACEN']
    },
    {
      label: 'Ventas',
      route: '/ventas',
      roles: ['ADMIN', 'CONTADOR', 'CAJERO']
    },
    {
      label: 'Caja',
      route: '/caja',
      roles: ['ADMIN', 'CAJERO', 'CONTADOR']
    },
    {
      label: 'Clientes',
      route: '/clientes',
      roles: ['ADMIN', 'CAJERO']
    },
    {
      label: 'Reportes',
      route: '/reportes',
      roles: ['ADMIN', 'CONTADOR']
    }
  ];

  private currentPage = 'Dashboard';

  constructor() {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.updatePageTitle(event.urlAfterRedirects);
        this.showUserMenu = false;
      }
    });
  }

  get filteredMenu(): MenuItem[] {
    return this.menu.filter(item =>
      item.roles.includes(this.user?.role || '')
    );
  }

  getIcon(label: string): string {
    const icons: { [key: string]: string } = {
      'Dashboard': 'dashboard',
      'Usuarios': 'people',
      'Productos': 'inventory_2',
      'Proveedores': 'local_shipping',
      'Inventario': 'warehouse',
      'Ventas': 'point_of_sale',
      'Caja': 'point_of_sale',
      'Clientes': 'person_outline',
      'Reportes': 'assessment'
    };
    return icons[label] || 'folder';
  }

  getCurrentPageTitle(): string {
    return this.currentPage;
  }

  private updatePageTitle(url: string): void {
    for (const item of this.menu) {
      if (url.includes(item.route)) {
        this.currentPage = item.label;
        return;
      }
    }
    this.currentPage = 'Dashboard';
  }

  toggleUserMenu(): void {
    this.showUserMenu = !this.showUserMenu;
  }

  goToProfile(): void {
    this.router.navigate(['/admin/profile']);
    this.showUserMenu = false;
  }

  goToChangePassword(): void {
    this.router.navigate(['/admin/cambiar-contraseña']);
    this.showUserMenu = false;
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }

  @HostListener('document:click', ['$event'])
  closeUserMenu(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    if (!target.closest('.user-section')) {
      this.showUserMenu = false;
    }
  }
}
