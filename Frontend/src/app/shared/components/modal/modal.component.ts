import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="modal-overlay" *ngIf="isOpen" (click)="onOverlayClick()">
      <div class="modal-container" [class]="'size-' + size" (click)="$event.stopPropagation()">
        <div class="modal-header">
          <h2>{{ title }}</h2>
          <button class="close-button" (click)="onClose()" *ngIf="showCloseButton">
            <span class="material-icons">close</span>
          </button>
        </div>

        <div class="modal-body">
          <ng-content></ng-content>
        </div>

        <div class="modal-footer" *ngIf="showFooter">
          <ng-content select="[footer]"></ng-content>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2000;
      padding: 1rem;
    }

    .modal-container {
      background-color: white;
      border-radius: 8px;
      box-shadow: 0 8px 16px rgba(0,0,0,0.2);
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .modal-container.size-sm {
      width: 100%;
      max-width: 400px;
    }

    .modal-container.size-md {
      width: 100%;
      max-width: 600px;
    }

    .modal-container.size-lg {
      width: 100%;
      max-width: 800px;
    }

    .modal-container.size-xl {
      width: 100%;
      max-width: 1000px;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1.5rem;
      border-bottom: 1px solid #e0e0e0;
    }

    .modal-header h2 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 600;
      color: #333;
    }

    .close-button {
      background: none;
      border: none;
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 4px;
      display: flex;
      align-items: center;
      color: #666;
    }

    .close-button:hover {
      background-color: #f5f5f5;
    }

    .modal-body {
      padding: 1.5rem;
      overflow-y: auto;
      flex: 1;
    }

    .modal-footer {
      padding: 1.5rem;
      border-top: 1px solid #e0e0e0;
      display: flex;
      justify-content: flex-end;
      gap: 0.5rem;
    }

    .material-icons {
      font-size: 1.5rem;
    }
  `]
})
export class ModalComponent {
  @Input() title = 'Modal';
  @Input() isOpen = false;
  @Input() size: 'sm' | 'md' | 'lg' | 'xl' = 'md';
  @Input() showCloseButton = true;
  @Input() showFooter = false;
  @Input() closeOnOverlayClick = true;

  @Output() close = new EventEmitter<void>();

  onClose() {
    this.close.emit();
  }

  onOverlayClick() {
    if (this.closeOnOverlayClick) {
      this.onClose();
    }
  }
}
