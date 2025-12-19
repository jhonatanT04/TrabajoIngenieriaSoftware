import { Routes } from '@angular/router';
import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
import { CajeroDashboardComponent } from './cajero-dashboard/cajero-dashboard.component';
import { AlmacenDashboardComponent } from './almacen-dashboard/almacen-dashboard.component';
import { ContadorDashboardComponent } from './contador-dashboard/contador-dashboard.component';
import { AuthService } from '../core/services/auth.service';

export const DASHBOARD_ROUTES: Routes = [
  {
    path: '',
    resolve: {
      roleRedirect: () => {
        const auth = new AuthService();
        const role = auth.getRole();

        switch (role) {
          case 'ADMIN': return 'admin';
          case 'CAJERO': return 'cajero';
          case 'ALMACEN': return 'almacen';
          case 'CONTADOR': return 'contador';
          default: return 'admin';
        }
      }
    },
    redirectTo: 'admin',
    pathMatch: 'full'
  },
  { path: 'admin', component: AdminDashboardComponent },
  { path: 'cajero', component: CajeroDashboardComponent },
  { path: 'almacen', component: AlmacenDashboardComponent },
  { path: 'contador', component: ContadorDashboardComponent }
];
