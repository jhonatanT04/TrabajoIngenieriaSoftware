import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ClienteService } from '../../core/services/cliente.service';

@Component({
  standalone: true,
  selector: 'app-cliente-create',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './cliente-create.component.html',
  styleUrls: ['./cliente-create.component.css']
})
export class ClienteCreateComponent {
  cliente = {
    nombre: '',
    cedula: '',
    email: '',
    telefono: '',
    direccion: '',
    ciudad: '',
    activo: true
  };

  guardando = false;

  constructor(
    private readonly clienteService: ClienteService,
    private readonly router: Router
  ) {}

  guardar(): void {
    if (this.guardando) return;
    this.guardando = true;

    this.clienteService.create(this.cliente).subscribe({
      next: () => this.router.navigate(['/clientes']),
      error: () => (this.guardando = false)
    });
  }

  cancelar(): void {
    this.router.navigate(['/clientes']);
  }
}
