import { Routes } from '@angular/router';
import { UsuarioListComponent } from './usuarios/usuario-list/usuario-list.component';
import { UsuarioCreateComponent } from './usuarios/usuario-create/usuario-create.component';
import { UsuarioEditComponent } from './usuarios/usuario-edit/usuario-edit.component';
import { UsuarioDetailComponent } from './usuarios/usuario-detail/usuario-detail.component';
import { RolListComponent } from './roles/rol-list/rol-list.component';
import { RolEditComponent } from './roles/rol-edit/rol-edit.component';
import { ImpuestosComponent } from './parametros/impuestos/impuestos.component';
import { MonedaComponent } from './parametros/moneda/moneda.component';
import { FormatosComponent } from './parametros/formatos/formatos.component';
import { DescuentosComponent } from './parametros/descuentos/descuentos.component';
import { AdminGuard } from './guards/admin.guard';

export const ADMIN_ROUTES: Routes = [
  { path: 'usuarios', component: UsuarioListComponent, canActivate: [AdminGuard] },
  { path: 'usuarios/create', component: UsuarioCreateComponent, canActivate: [AdminGuard] },
  { path: 'usuarios/:id', component: UsuarioDetailComponent, canActivate: [AdminGuard] },
  { path: 'usuarios/:id/edit', component: UsuarioEditComponent, canActivate: [AdminGuard] },

  { path: 'roles', component: RolListComponent, canActivate: [AdminGuard] },
  { path: 'roles/:id/edit', component: RolEditComponent, canActivate: [AdminGuard] },

  { path: 'parametros/impuestos', component: ImpuestosComponent, canActivate: [AdminGuard] },
  { path: 'parametros/moneda', component: MonedaComponent, canActivate: [AdminGuard] },
  { path: 'parametros/formatos', component: FormatosComponent, canActivate: [AdminGuard] },
  { path: 'parametros/descuentos', component: DescuentosComponent, canActivate: [AdminGuard] },

  { path: '', redirectTo: 'usuarios', pathMatch: 'full' }
];
