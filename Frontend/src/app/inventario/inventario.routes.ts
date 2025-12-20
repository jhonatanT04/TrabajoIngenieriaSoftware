import { Routes } from '@angular/router';
import { StockListComponent } from './stock/stock-list/stock-list.component';
import { StockAjusteComponent } from './stock/stock-ajuste/stock-ajuste.component';
import { MovimientoListComponent } from './movimientos/movimiento-list/movimiento-list.component';

export const INVENTARIO_ROUTES: Routes = [
  { path: 'stock', component: StockListComponent },
  { path: 'stock/ajuste/:id', component: StockAjusteComponent },
  { path: 'movimientos', component: MovimientoListComponent },
  { path: '', redirectTo: 'stock', pathMatch: 'full' }
];
