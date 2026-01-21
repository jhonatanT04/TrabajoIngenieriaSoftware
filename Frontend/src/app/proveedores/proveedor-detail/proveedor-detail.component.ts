import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { ProveedorService } from '../../core/services/proveedor.service';
import { Proveedor } from '../../core/models/producto.model';

@Component({
  standalone: true,
  selector: 'app-proveedor-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './proveedor-detail.component.html',
  styleUrls: ['./proveedor-detail.component.css']
})
export class ProveedorDetailComponent implements OnInit {
  proveedor: Proveedor | null = null;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private proveedorService: ProveedorService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadProveedor(id);
    } else {
      this.error = 'ID de proveedor no válido';
      this.loading = false;
    }
  }

  loadProveedor(id: string): void {
    this.loading = true;
    this.proveedorService.getById(id).subscribe({
      next: (proveedor) => {
        this.proveedor = proveedor;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando proveedor:', err);
        this.error = 'Error al cargar el proveedor';
        this.loading = false;
      }
    });
  }

  volver(): void {
    this.router.navigate(['/proveedores']);
  }

  editar(): void {
    if (this.proveedor?.id) {
      this.router.navigate(['/proveedores/editar', this.proveedor.id]);
    }
  }
}
