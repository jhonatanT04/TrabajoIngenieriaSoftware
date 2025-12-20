import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ProveedorService } from '../../core/services/proveedor.service';

@Component({
  standalone: true,
  selector: 'app-proveedor-create',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './proveedor-create.component.html',
  styleUrls: ['./proveedor-create.component.css']
})
export class ProveedorCreateComponent {
  proveedor = {
    nombre: '',
    contacto: '',
    email: '',
    telefono: '',
    ciudad: '',
    direccion: '',
    activo: true
  };

  guardando = false;

  constructor(
    private readonly proveedorService: ProveedorService,
    private readonly router: Router
  ) {}

  guardar(): void {
    if (this.guardando) return;
    this.guardando = true;

    this.proveedorService.create(this.proveedor).subscribe({
      next: () => this.router.navigate(['/proveedores']),
      error: () => (this.guardando = false)
    });
  }

  cancelar(): void {
    this.router.navigate(['/proveedores']);
  }
}
