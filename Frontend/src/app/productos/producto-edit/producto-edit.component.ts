import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductoService } from '../../core/services/producto.service';
import { Producto, Categoria, Brand } from '../../core/models/producto.model';

@Component({
  standalone: true,
  selector: 'app-producto-edit',
  imports: [CommonModule, FormsModule],
  templateUrl: './producto-edit.component.html'
})
export class ProductoEditComponent implements OnInit {
  producto?: Producto;
  categorias: Categoria[] = [];
  marcas: Brand[] = [];
  loading = true;
  saving = false;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private productoService: ProductoService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id')!;

    this.productoService.getById(id).subscribe({
      next: (producto) => {
        this.producto = { ...producto };
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando producto:', err);
        this.error = 'Error al cargar el producto';
        this.loading = false;
      }
    });

    this.loadCategorias();
    this.loadMarcas();
  }

  loadCategorias(): void {
    this.productoService.getCategorias().subscribe({
      next: (categorias) => {
        this.categorias = categorias;
      },
      error: (err) => {
        console.error('Error cargando categorías:', err);
      }
    });
  }

  loadMarcas(): void {
    this.productoService.getMarcas().subscribe({
      next: (marcas) => {
        this.marcas = marcas;
      },
      error: (err) => {
        console.error('Error cargando marcas:', err);
      }
    });
  }

  guardar(): void {
    if (!this.producto) return;

    this.saving = true;
    this.error = '';
    
    this.productoService.update(this.producto.id!, this.producto).subscribe({
      next: () => {
        this.router.navigate(['/productos']);
      },
      error: (err) => {
        console.error('Error actualizando producto:', err);
        this.error = 'Error al actualizar el producto';
        this.saving = false;
      }
    });
  }
}
