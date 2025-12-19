import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-not-found',
  imports: [CommonModule, RouterModule],
  template: `
    <div class="not-found-container">
      <h1>404</h1>
      <h2>Página no encontrada</h2>
      <p>Lo sentimos, la ruta que intentas acceder no existe.</p>
      <a routerLink="/">Volver al inicio</a>
    </div>
  `,
  styles: [`
    .not-found-container {
      text-align: center;
      margin-top: 100px;
      font-family: Arial, sans-serif;
      color: #1e293b;
    }

    h1 {
      font-size: 6rem;
      margin-bottom: 20px;
      color: #ef4444;
    }

    h2 {
      font-size: 2rem;
      margin-bottom: 10px;
    }

    p {
      font-size: 1.2rem;
      margin-bottom: 20px;
    }

    a {
      text-decoration: none;
      color: #2563eb;
      font-weight: bold;
    }

    a:hover {
      text-decoration: underline;
    }
  `]
})
export class NotFoundComponent {}
