import { Routes } from '@angular/router';

export const POS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./pos-layout/pos-layout.component')
        .then(m => m.PosLayoutComponent),
    children: [
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
      }
    ]
  }
];
