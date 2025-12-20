import { Routes } from '@angular/router';

export const POS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./pos-home/pos-home.component')
        .then(m => m.PosHomeComponent)
  },
  {
    path: 'pago',
    loadComponent: () =>
      import('./pos-pago/pos-pago.component')
        .then(m => m.PosPagoComponent)
  },
  {
    path: 'ticket',
    loadComponent: () =>
      import('./pos-ticket/pos-ticket.component')
        .then(m => m.PosTicketComponent)
  },
  {
    path: 'profile',
    loadComponent: () =>
      import('../admin/profile/profile.component')
        .then(m => m.ProfileComponent)
  },
  {
    path: 'cambiar-password',
    loadComponent: () =>
      import('../admin/change-password/change-password.component')
        .then(m => m.ChangePasswordComponent)
  }
];
