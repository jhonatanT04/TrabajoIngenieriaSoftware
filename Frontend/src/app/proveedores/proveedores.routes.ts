import { Routes } from '@angular/router';

import { ProveedorListComponent } from './proveedor-list/proveedor-list.component';
import { ProveedorCreateComponent } from './proveedor-create/proveedor-create.component';
import { ProveedorEditComponent } from './proveedor-edit/proveedor-edit.component';
import { ProveedorDetailComponent } from './proveedor-detail/proveedor-detail.component';

export const PROVEEDORES_ROUTES: Routes = [
  { path: '', component: ProveedorListComponent },
  { path: 'nuevo', component: ProveedorCreateComponent },
  { path: 'editar/:id', component: ProveedorEditComponent },
  { path: 'detalle/:id', component: ProveedorDetailComponent }
];
