import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // 👈 FALTA ESTO
import { ActivatedRoute } from '@angular/router';
import { FidelidadService } from '../../core/services/fidelidad.service';

@Component({
  standalone: true,
  selector: 'app-fidelidad',
  imports: [CommonModule, FormsModule], // 👈 AGRÉGALO AQUÍ
  templateUrl: './fidelidad.component.html'
})
export class FidelidadComponent {

  puntos: number = 0;
  id: number;

  constructor(
    route: ActivatedRoute,
    private fidelidad: FidelidadService
  ) {
    this.id = +route.snapshot.paramMap.get('id')!;
  }

  canjear(): void {
    this.fidelidad.canjear(this.id, this.puntos);
    this.puntos = 0;
  }
}
