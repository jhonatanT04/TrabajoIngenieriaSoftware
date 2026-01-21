import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { ProductoService } from '../../core/services/producto.service';
import { Producto } from '../../core/models/producto.model';

@Component({
  standalone: true,
  selector: 'app-producto-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './producto-detail.component.html',
  styleUrls: ['./producto-detail.component.css']
})
export class ProductoDetailComponent implements OnInit {
  producto: Producto | null = null;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private productoService: ProductoService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadProducto(id);
    } else {
      this.error = 'ID de producto no válido';
      this.loading = false;
    }
  }

  loadProducto(id: string): void {
    this.loading = true;
    this.productoService.getById(id).subscribe({
      next: (producto) => {
        this.producto = producto;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando producto:', err);
        this.error = 'Error al cargar el producto';
        this.loading = false;
      }
    });
  }

  volver(): void {
    this.router.navigate(['/productos']);
  }

  editar(): void {
    if (this.producto?.id) {
      this.router.navigate(['/productos/editar', this.producto.id]);
    }
  }
}
