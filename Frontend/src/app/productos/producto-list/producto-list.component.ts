import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-producto-list',
  imports: [CommonModule],
  template: `<h2>Productos (lista placeholder)</h2>`
})
export class ProductoListComponent {}
