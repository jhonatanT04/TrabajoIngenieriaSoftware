import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ClientesService } from '../../core/services/clientes.service';

@Component({
  standalone: true,
  selector: 'app-cliente-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './cliente-detail.component.html'
})
export class ClienteDetailComponent {

  cliente: any;

  constructor(
    route: ActivatedRoute,
    service: ClientesService
  ) {
    this.cliente = service.getById(+route.snapshot.paramMap.get('id')!);
  }
}
