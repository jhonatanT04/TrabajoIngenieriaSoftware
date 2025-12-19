import { Routes } from '@angular/router';

import { AperturaComponent } from './apertura/apertura.component';
import { CierreComponent } from './cierre/cierre.component';
import { ArqueoComponent } from './arqueo/arqueo.component';
import { MovimientosCajaComponent } from './movimientos/movimientos.component';

export const CAJA_ROUTES: Routes = [
  { path: 'apertura', component: AperturaComponent },
  { path: 'cierre', component: CierreComponent },
  { path: 'arqueo', component: ArqueoComponent },
  { path: 'movimientos', component: MovimientosCajaComponent },
  { path: '', redirectTo: 'apertura', pathMatch: 'full' }
];
