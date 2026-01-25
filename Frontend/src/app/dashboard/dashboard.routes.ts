import { Routes } from '@angular/router';
import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
import { CajeroDashboardComponent } from './cajero-dashboard/cajero-dashboard.component';
import { AlmacenDashboardComponent } from './almacen-dashboard/almacen-dashboard.component';
import { ContadorDashboardComponent } from './contador-dashboard/contador-dashboard.component';
import { DashboardRedirectComponent } from './dashboard-redirect.component';

export const DASHBOARD_ROUTES: Routes = [
  {
    path: '',
    component: DashboardRedirectComponent,
    pathMatch: 'full'
  },
  { path: 'admin', component: AdminDashboardComponent },
  { path: 'cajero', component: CajeroDashboardComponent },
  { path: 'almacen', component: AlmacenDashboardComponent },
  { path: 'contador', component: ContadorDashboardComponent }
];
