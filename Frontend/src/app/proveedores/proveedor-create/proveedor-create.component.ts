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
    ruc: '',
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

    const payload = {
      business_name: this.proveedor.nombre?.trim() || '',
      tax_id: this.proveedor.ruc?.trim() || '',
      representative_name: this.proveedor.contacto?.trim() || undefined,
      email: this.proveedor.email?.trim() || undefined,
      phone: this.proveedor.telefono?.trim() || undefined,
      address: this.proveedor.direccion?.trim() || undefined,
      city: this.proveedor.ciudad?.trim() || undefined,
      is_active: !!this.proveedor.activo
    };

    this.proveedorService.create(payload).subscribe({
      next: () => this.router.navigate(['/proveedores']),
      error: () => (this.guardando = false)
    });
  }

  cancelar(): void {
    this.router.navigate(['/proveedores']);
  }
}
