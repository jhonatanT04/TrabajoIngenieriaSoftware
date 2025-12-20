import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-producto-create',
  imports: [CommonModule, FormsModule],
  templateUrl: './producto-create.component.html',
  styleUrls: ['./producto-create.component.css']
})
export class ProductoCreateComponent {
  producto: any = { activo: true };

  constructor(private router: Router) {}

  guardar() {
    // Aquí se conectará con el backend; por ahora solo navega
    this.router.navigate(['/productos']);
  }
}
