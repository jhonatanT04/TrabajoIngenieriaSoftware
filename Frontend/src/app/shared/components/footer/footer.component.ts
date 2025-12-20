import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

/**
 * Componente Footer
 * Pie de página de la aplicación
 */
@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  template: `
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-left">
          <span>&copy; {{ currentYear }} Sistema de Gestión de Minimercado</span>
        </div>
        <div class="footer-right">
          <span>Versión {{ version }}</span>
        </div>
      </div>
    </footer>
  `,
  styles: [`
    .footer {
      background-color: #f5f5f5;
      border-top: 1px solid #e0e0e0;
      padding: 1rem 1.5rem;
      margin-top: auto;
    }

    .footer-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
      font-size: 0.875rem;
      color: #666;
    }

    @media (max-width: 768px) {
      .footer-content {
        flex-direction: column;
        gap: 0.5rem;
        text-align: center;
      }
    }
  `]
})
export class FooterComponent {
  currentYear = new Date().getFullYear();
  version = '1.0.0-beta';
}
