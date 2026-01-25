import { Routes } from '@angular/router';
import { ReportesListComponent } from './reportes-list/reportes-list.component';
import { ReportesCreateComponent } from './reportes-create/reportes-create.component';
import { ReporteVentasComponent } from './ventas/reporte-ventas/reporte-ventas.component';
import { ReporteCajaComponent } from './caja/reporte-caja/reporte-caja.component';
import { ReporteInventarioComponent } from './inventario/reporte-inventario/reporte-inventario.component';
import { ReporteClientesComponent } from './clientes/reporte-clientes/reporte-clientes.component';

export const REPORTES_ROUTES: Routes = [
  { path: '', component: ReportesListComponent },
  { path: 'nuevo', component: ReportesCreateComponent },
  { path: 'ventas', component: ReporteVentasComponent },
  { path: 'caja', component: ReporteCajaComponent },
  { path: 'inventario', component: ReporteInventarioComponent },
  { path: 'clientes', component: ReporteClientesComponent }
];
