import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CajaService } from '../../core/services/caja.service';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-cierre',
  imports: [CommonModule],
  templateUrl: './cierre.component.html'
})
export class CierreComponent {

  constructor(
    public cajaService: CajaService,
    private router: Router
  ) {}

  cerrar() {
    this.cajaService.cerrarCaja();
    this.router.navigate(['/dashboard']);
  }
}
