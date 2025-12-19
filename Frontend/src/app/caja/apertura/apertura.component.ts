import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CajaService } from '../../core/services/caja.service';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-apertura',
  imports: [CommonModule, FormsModule],
  templateUrl: './apertura.component.html'
})
export class AperturaComponent {

  monto = 0;

  constructor(
    public cajaService: CajaService,
    private router: Router
  ) {}

  abrir() {
    this.cajaService.abrirCaja(this.monto);
    this.router.navigate(['/caja/arqueo']);
  }
}
