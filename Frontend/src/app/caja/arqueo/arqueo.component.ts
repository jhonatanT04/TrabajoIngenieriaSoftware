import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CajaService } from '../../core/services/caja.service';

@Component({
  standalone: true,
  selector: 'app-arqueo',
  imports: [CommonModule],
  templateUrl: './arqueo.component.html'
})
export class ArqueoComponent {

  constructor(public cajaService: CajaService) {}
}
