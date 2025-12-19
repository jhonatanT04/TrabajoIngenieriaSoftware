import { Routes } from '@angular/router';

import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'auth', pathMatch: 'full' },

  /* =====================
     AUTH (PÚBLICO)
  ====================== */
  {
    path: 'auth',
    loadChildren: () =>
      import('./auth/auth.routes').then(m => m.AUTH_ROUTES)
  },

  /* =====================
     ADMIN / SISTEMA
  ====================== */
  {
    path: '',
    loadComponent: () =>
      import('./layout/admin-layout/admin-layout.component')
        .then(c => c.AdminLayoutComponent),
    canActivate: [AuthGuard],
    children: [

      /* DASHBOARD */
      {
        path: 'dashboard',
        loadChildren: () =>
          import('./dashboard/dashboard.routes')
            .then(m => m.DASHBOARD_ROUTES)
      },

      /* ADMIN (SOLO ADMINISTRADOR) */
      {
        path: 'admin',
        canActivate: [RoleGuard],
        data: { roles: ['ADMIN'] },
        loadChildren: () =>
          import('./admin/admin.routes')
            .then(m => m.ADMIN_ROUTES)
      },

      /* PRODUCTOS (ADMIN / ALMACÉN) */
      {
        path: 'productos',
        canActivate: [RoleGuard],
        data: { roles: ['ADMIN', 'ALMACEN'] },
        loadChildren: () =>
          import('./productos/productos.routes')
            .then(m => m.PRODUCTOS_ROUTES)
      },

      /* INVENTARIO */
      {
        path: 'inventario',
        canActivate: [RoleGuard],
        data: { roles: ['ADMIN', 'ALMACEN'] },
        loadChildren: () =>
          import('./inventario/inventario.routes')
            .then(m => m.INVENTARIO_ROUTES)
      },

      /* CLIENTES */
      {
        path: 'clientes',
        canActivate: [RoleGuard],
        data: { roles: ['ADMIN', 'CAJERO'] },
        loadChildren: () =>
          import('./clientes/clientes.routes')
            .then(m => m.CLIENTES_ROUTES)
      },

      /* REPORTES */
      {
        path: 'reportes',
        canActivate: [RoleGuard],
        data: { roles: ['ADMIN', 'CONTADOR'] },
        loadChildren: () =>
          import('./reportes/reportes.routes')
            .then(m => m.REPORTES_ROUTES)
      },

      { path: '', redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  },

  /* =====================
     POS (SOLO CAJERO)
  ====================== */
  {
    path: 'pos',
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['CAJERO'] },
    loadComponent: () =>
      import('./layout/pos-layout/pos-layout.component')
        .then(c => c.PosLayoutComponent),
    loadChildren: () =>
      import('./pos/pos.routes')
        .then(m => m.POS_ROUTES)
  },

  /* =====================
     404
  ====================== */
  {
    path: '**',
    loadComponent: () =>
      import('./not-found/not-found.component')
        .then(c => c.NotFoundComponent)
  }
];
