import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ClientesService } from '../../core/services/clientes.service';

@Component({
  standalone: true,
  selector: 'app-cliente-edit',
  imports: [CommonModule, FormsModule],
  template: `
    <h2>Editar Cliente</h2>
    <form (ngSubmit)="guardar()">
      <label>Nombre: <input [(ngModel)]="cliente.nombre" name="nombre" /></label>
      <button type="submit">Guardar</button>
    </form>
  `
})
export class ClienteEditComponent {
  cliente: any;

  constructor(
    route: ActivatedRoute,
    private service: ClientesService,
    private router: Router
  ) {
    const id = +route.snapshot.paramMap.get('id')!;
    this.cliente = { ...this.service.getById(id) };
  }

  guardar() {
    this.service.update(this.cliente);
    this.router.navigate(['/clientes']);
  }
}
