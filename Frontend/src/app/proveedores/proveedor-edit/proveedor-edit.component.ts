import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ProveedorService } from '../../core/services/proveedor.service';
import { Proveedor } from '../../core/models/producto.model';

@Component({
  standalone: true,
  selector: 'app-proveedor-edit',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './proveedor-edit.component.html'
})
export class ProveedorEditComponent implements OnInit {
  proveedor?: Proveedor;
  loading = true;
  saving = false;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private proveedorService: ProveedorService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id')!;

    this.proveedorService.getById(id).subscribe({
      next: (proveedor) => {
        this.proveedor = { ...proveedor };
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando proveedor:', err);
        this.error = 'Error al cargar el proveedor';
        this.loading = false;
      }
    });
  }

  guardar(): void {
    if (!this.proveedor) return;

    this.saving = true;
    this.error = '';

    this.proveedorService.update(this.proveedor.id, this.proveedor).subscribe({
      next: () => {
        this.router.navigate(['/proveedores']);
      },
      error: (err) => {
        console.error('Error actualizando proveedor:', err);
        this.error = 'Error al actualizar el proveedor';
        this.saving = false;
      }
    });
  }

  cancelar(): void {
    this.router.navigate(['/proveedores']);
  }
}
