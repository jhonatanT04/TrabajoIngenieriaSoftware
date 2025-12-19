import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClientesService } from '../../core/services/clientes.service';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-cliente-create',
  imports: [CommonModule, FormsModule],
  templateUrl: './cliente-create.component.html'
})
export class ClienteCreateComponent {

  cliente: any = {};

  constructor(
    private service: ClientesService,
    private router: Router
  ) {}

  guardar() {
    this.service.create(this.cliente);
    this.router.navigate(['/clientes']);
  }
}
