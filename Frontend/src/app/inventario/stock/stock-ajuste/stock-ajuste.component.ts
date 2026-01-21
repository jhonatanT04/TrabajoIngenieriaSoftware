import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { InventarioService } from '../../../core/services/inventario.service';
import { ProductoService } from '../../../core/services/producto.service';

@Component({
  standalone: true,
  selector: 'app-stock-ajuste',
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './stock-ajuste.component.html',
  styleUrls: ['./stock-ajuste.component.css']
})
export class StockAjusteComponent implements OnInit {
  producto: any;
  form!: FormGroup;
  loading = false;
  productId = '';
  submitted = false;
  successMessage = '';
  errorMessage = '';
  stockActual = 0;
  tiposAjuste = [
    { id: 'correccion_inventario', label: 'Corrección de Inventario' },
    { id: 'devolucion', label: 'Devolución' },
    { id: 'perdida', label: 'Pérdida' },
    { id: 'ajuste_fisico', label: 'Ajuste Físico' },
    { id: 'otro', label: 'Otro' }
  ];

  constructor(
    private route: ActivatedRoute,
    private inventario: InventarioService,
    private productoService: ProductoService,
    private router: Router,
    private fb: FormBuilder
  ) {
    this.productId = route.snapshot.paramMap.get('id')!;
    this.initForm();
  }

  ngOnInit() {
    this.loadProduct();
  }

  initForm() {
    this.form = this.fb.group({
      nuevaCantidad: [0, [Validators.required, Validators.min(0)]],
      razon: ['', Validators.required],
      tipoAjuste: ['', Validators.required],
      observaciones: ['']
    });
  }

  loadProduct() {
    this.loading = true;
    this.productoService.getById(this.productId).subscribe({
      next: (producto) => {
        this.producto = producto;
        // Cargar stock actual del inventario
        this.inventario.getByProduct(this.productId).subscribe({
          next: (inventario) => {
            this.stockActual = inventario.quantity || 0;
            this.form.patchValue({ nuevaCantidad: this.stockActual });
            this.loading = false;
          },
          error: () => {
            // Si no hay inventario, usar 0
            this.stockActual = 0;
            this.form.patchValue({ nuevaCantidad: this.stockActual });
            this.loading = false;
          }
        });
      },
      error: (err) => {
        this.errorMessage = 'Error cargando el producto';
        this.loading = false;
      }
    });
  }

  get diferencia(): number {
    const nueva = this.form.get('nuevaCantidad')?.value || 0;
    return nueva - this.stockActual;
  }

  get f() {
    return this.form.controls;
  }

  ajustar() {
    this.submitted = true;
    this.successMessage = '';
    this.errorMessage = '';

    if (this.form.invalid) {
      this.errorMessage = 'Por favor complete todos los campos requeridos';
      return;
    }

    const nuevaCantidad = this.form.get('nuevaCantidad')?.value;
    if (nuevaCantidad < 0) {
      this.errorMessage = 'La cantidad no puede ser negativa';
      return;
    }

    this.loading = true;
    this.inventario.adjustInventory({
      product_id: this.productId,
      new_quantity: nuevaCantidad,
      reason: this.form.get('razon')?.value
    }).subscribe({
      next: () => {
        this.loading = false;
        this.successMessage = 'Ajuste realizado exitosamente';
        setTimeout(() => {
          this.router.navigate(['/inventario/stock']);
        }, 1500);
      },
      error: (err) => {
        this.errorMessage = err.error?.detail || 'Error al realizar el ajuste';
        this.loading = false;
      }
    });
  }

  volver() {
    this.router.navigate(['/inventario/stock']);
  }

  resetForm() {
    this.form.patchValue({
      nuevaCantidad: this.stockActual,
      razon: '',
      tipoAjuste: '',
      observaciones: ''
    });
    this.submitted = false;
    this.successMessage = '';
    this.errorMessage = '';
  }
}
