import { Routes } from '@angular/router';

import { ProductoListComponent } from './producto-list/producto-list.component';
import { ProductoCreateComponent } from './producto-create/producto-create.component';
import { ProductoEditComponent } from './producto-edit/producto-edit.component';
import { ProductoDetailComponent } from './producto-detail/producto-detail.component';

export const PRODUCTOS_ROUTES: Routes = [
  { path: '', component: ProductoListComponent },
  { path: 'nuevo', component: ProductoCreateComponent },
  { path: 'editar/:id', component: ProductoEditComponent },
  { path: 'detalle/:id', component: ProductoDetailComponent }
];
