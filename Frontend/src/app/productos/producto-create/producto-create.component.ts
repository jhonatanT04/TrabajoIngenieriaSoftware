import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ProductoService } from '../../core/services/producto.service';
import { ProductoCreateRequest, Categoria, Brand } from '../../core/models/producto.model';

@Component({
  standalone: true,
  selector: 'app-producto-create',
  imports: [CommonModule, FormsModule],
  templateUrl: './producto-create.component.html',
  styleUrls: ['./producto-create.component.css']
})
export class ProductoCreateComponent implements OnInit {
  producto: ProductoCreateRequest = {
    sku: '',
    name: '',
    description: '',
    category_id: undefined,
    brand_id: undefined,
    main_supplier_id: undefined,
    unit_of_measure: 'unidad',
    sale_price: 0,
    cost_price: 0,
    tax_rate: 0,
    stock_min: 0,
    stock_max: 0,
    is_active: true
  };

  categorias: Categoria[] = [];
  marcas: Brand[] = [];
  loading = false;
  error = '';

  constructor(
    private router: Router,
    private productoService: ProductoService
  ) {}

  ngOnInit(): void {
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
    this.loading = true;
    this.error = '';
    
    this.productoService.create(this.producto).subscribe({
      next: () => {
        this.router.navigate(['/productos']);
      },
      error: (err) => {
        console.error('Error creando producto:', err);
        this.error = 'Error al crear el producto. Verifique los datos.';
        this.loading = false;
      }
    });
  }
}
