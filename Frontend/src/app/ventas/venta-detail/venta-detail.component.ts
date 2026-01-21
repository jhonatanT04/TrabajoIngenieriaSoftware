import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { VentaService } from '../../core/services/venta.service';

@Component({
  standalone: true,
  selector: 'app-venta-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './venta-detail.component.html',
  styleUrls: ['./venta-detail.component.css']
})
export class VentaDetailComponent implements OnInit {
  venta: any = null;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private ventaService: VentaService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    console.log('📍 ID del parámetro de ruta:', id);
    if (id) {
      this.cargarVenta(id);
    } else {
      this.error = 'No se recibió ID de venta';
      this.loading = false;
    }
  }

  cargarVenta(id: string): void {
    console.log('🔄 Cargando venta con ID:', id);
    this.ventaService.getById(id).subscribe({
      next: (venta) => {
        console.log('✅ Venta cargada:', venta);
        this.venta = venta;
        this.loading = false;
      },
      error: (err) => {
        console.error('❌ Error cargando venta:', err);
        this.error = 'No se pudo cargar la venta: ' + (err.error?.detail || err.message);
        this.loading = false;
      }
    });
  }

  volver(): void {
    this.router.navigate(['/ventas']);
  }
}
