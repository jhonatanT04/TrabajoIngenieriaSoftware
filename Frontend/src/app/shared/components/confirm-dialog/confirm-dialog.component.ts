import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dialog-overlay" *ngIf="isOpen">
      <div class="dialog-container">
        <div class="dialog-icon" [class]="'type-' + type">
          <span class="material-icons">{{ getIcon() }}</span>
        </div>

        <h2 class="dialog-title">{{ title }}</h2>
        <p class="dialog-message">{{ message }}</p>

        <div class="dialog-actions">
          <button class="btn btn-secondary" (click)="onCancel()">
            {{ cancelText }}
          </button>
          <button class="btn" [class]="'btn-' + type" (click)="onConfirm()">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dialog-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 3000;
      padding: 1rem;
    }

    .dialog-container {
      background-color: white;
      border-radius: 8px;
      padding: 2rem;
      max-width: 400px;
      width: 100%;
      box-shadow: 0 8px 16px rgba(0,0,0,0.2);
      text-align: center;
    }

    .dialog-icon {
      width: 64px;
      height: 64px;
      margin: 0 auto 1.5rem;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .dialog-icon.type-warning {
      background-color: #fff3cd;
      color: #856404;
    }

    .dialog-icon.type-danger {
      background-color: #f8d7da;
      color: #721c24;
    }

    .dialog-icon.type-info {
      background-color: #d1ecf1;
      color: #0c5460;
    }

    .dialog-icon.type-success {
      background-color: #d4edda;
      color: #155724;
    }

    .dialog-icon .material-icons {
      font-size: 2rem;
    }

    .dialog-title {
      margin: 0 0 1rem;
      font-size: 1.5rem;
      font-weight: 600;
      color: #333;
    }

    .dialog-message {
      margin: 0 0 2rem;
      color: #666;
      line-height: 1.5;
    }

    .dialog-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
    }

    .btn {
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 4px;
      font-size: 1rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn-secondary {
      background-color: #6c757d;
      color: white;
    }

    .btn-secondary:hover {
      background-color: #5a6268;
    }

    .btn-warning {
      background-color: #ffc107;
      color: #333;
    }

    .btn-warning:hover {
      background-color: #e0a800;
    }

    .btn-danger {
      background-color: #dc3545;
      color: white;
    }

    .btn-danger:hover {
      background-color: #c82333;
    }

    .btn-info {
      background-color: #17a2b8;
      color: white;
    }

    .btn-info:hover {
      background-color: #138496;
    }

    .btn-success {
      background-color: #28a745;
      color: white;
    }

    .btn-success:hover {
      background-color: #218838;
    }
  `]
})
export class ConfirmDialogComponent {
  @Input() isOpen = false;
  @Input() title = '¿Está seguro?';
  @Input() message = '¿Desea continuar con esta acción?';
  @Input() type: 'warning' | 'danger' | 'info' | 'success' = 'warning';
  @Input() confirmText = 'Confirmar';
  @Input() cancelText = 'Cancelar';

  @Output() confirm = new EventEmitter<void>();
  @Output() cancel = new EventEmitter<void>();

  getIcon(): string {
    const icons = {
      warning: 'warning',
      danger: 'error',
      info: 'info',
      success: 'check_circle'
    };
    return icons[this.type];
  }

  onConfirm() {
    this.confirm.emit();
  }

  onCancel() {
    this.cancel.emit();
  }
}
