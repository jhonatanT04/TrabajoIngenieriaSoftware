import { Routes } from '@angular/router';

import { VentaListComponent } from './venta-list/venta-list.component';
import { VentaDetailComponent } from './venta-detail/venta-detail.component';
import { VentaCreateComponent } from './venta-create/venta-create.component';

import { PromocionListComponent } from './promociones/promocion-list/promocion-list.component';
import { PromocionCreateComponent } from './promociones/promocion-create/promocion-create.component';
import { PromocionEditComponent } from './promociones/promocion-edit/promocion-edit.component';

export const VENTAS_ROUTES: Routes = [
  { path: '', component: VentaListComponent },
  { path: 'nuevo', component: VentaCreateComponent },
  { path: 'detalle/:id', component: VentaDetailComponent },

  { path: 'promociones', component: PromocionListComponent },
  { path: 'promociones/nuevo', component: PromocionCreateComponent },
  { path: 'promociones/editar/:id', component: PromocionEditComponent }
];
