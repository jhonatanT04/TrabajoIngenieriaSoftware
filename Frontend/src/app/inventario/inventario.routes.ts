import { Routes } from '@angular/router';

import { StockListComponent } from './stock/stock-list/stock-list.component';
import { StockAjusteComponent } from './stock/stock-ajuste/stock-ajuste.component';

import { RecepcionListComponent } from './recepcion/recepcion-list/recepcion-list.component';
import { RecepcionCreateComponent } from './recepcion/recepcion-create/recepcion-create.component';
import { RecepcionDetailComponent } from './recepcion/recepcion-detail/recepcion-detail.component';

import { MovimientoListComponent } from './movimientos/movimiento-list/movimiento-list.component';

export const INVENTARIO_ROUTES: Routes = [
  { path: 'stock', component: StockListComponent },
  { path: 'stock/ajuste', component: StockAjusteComponent },

  { path: 'recepcion', component: RecepcionListComponent },
  { path: 'recepcion/nuevo', component: RecepcionCreateComponent },
  { path: 'recepcion/detalle/:id', component: RecepcionDetailComponent },

  { path: 'movimientos', component: MovimientoListComponent },

  { path: '', redirectTo: 'stock', pathMatch: 'full' }
];
