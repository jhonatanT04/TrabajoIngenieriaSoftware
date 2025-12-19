import { Component, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
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
      roles: ['ADMIN']
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
      roles: ['ADMIN', 'CONTADOR']
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

  get filteredMenu(): MenuItem[] {
    return this.menu.filter(item =>
      item.roles.includes(this.user?.role)
    );
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}
