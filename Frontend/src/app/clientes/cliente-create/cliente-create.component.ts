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

    const payload = {
      first_name: this.cliente.nombre.split(' ')[0] || '',
      last_name: this.cliente.nombre.split(' ').slice(1).join(' ') || this.cliente.nombre,
      document_number: this.cliente.cedula,
      email: this.cliente.email || undefined,
      phone: this.cliente.telefono || undefined,
      address: this.cliente.direccion || undefined,
      city: this.cliente.ciudad || undefined,
      is_active: this.cliente.activo
    };

    this.clienteService.create(payload).subscribe({
      next: () => this.router.navigate(['/clientes']),
      error: (err) => {
        console.error('Error creando cliente:', err);
        this.guardando = false;
      }
    });
  }

  cancelar(): void {
    this.router.navigate(['/clientes']);
  }
}
