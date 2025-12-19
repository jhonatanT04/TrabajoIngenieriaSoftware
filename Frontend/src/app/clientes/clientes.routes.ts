import { Routes } from '@angular/router';
import { ClienteListComponent } from './cliente-list/cliente-list.component';
import { ClienteCreateComponent } from './cliente-create/cliente-create.component';
import { ClienteEditComponent } from './cliente-edit/cliente-edit.component';
import { ClienteDetailComponent } from './cliente-detail/cliente-detail.component';
import { FidelidadComponent } from './fidelidad/fidelidad.component';

export const CLIENTES_ROUTES: Routes = [
  { path: '', component: ClienteListComponent },
  { path: 'create', component: ClienteCreateComponent },
  { path: ':id', component: ClienteDetailComponent },
  { path: ':id/edit', component: ClienteEditComponent },
  { path: ':id/fidelidad', component: FidelidadComponent }
];
