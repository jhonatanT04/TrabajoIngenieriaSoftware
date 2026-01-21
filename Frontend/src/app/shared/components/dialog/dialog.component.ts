import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DialogService, DialogState } from '../../services/dialog.service';

@Component({
  selector: 'app-dialog',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dialog-overlay" *ngIf="dialog?.isOpen" (click)="onCancel()">
      <div class="dialog-box" (click)="$event.stopPropagation()">
        <div class="dialog-header">
          <h3>{{ dialog?.title }}</h3>
          <button class="close-btn" (click)="onCancel()">✕</button>
        </div>
        
        <div class="dialog-body">
          <p>{{ dialog?.message }}</p>
        </div>
        
        <div class="dialog-footer">
          <button class="btn btn-secondary" (click)="onCancel()">
            {{ dialog?.cancelText }}
          </button>
          <button class="btn btn-primary" (click)="onConfirm()">
            {{ dialog?.confirmText }}
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
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      animation: fadeIn 0.2s ease-in-out;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }

    .dialog-box {
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
      max-width: 400px;
      width: 90%;
      animation: slideUp 0.3s ease-out;
    }

    @keyframes slideUp {
      from {
        transform: translateY(20px);
        opacity: 0;
      }
      to {
        transform: translateY(0);
        opacity: 1;
      }
    }

    .dialog-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px;
      border-bottom: 1px solid #e5e7eb;
    }

    .dialog-header h3 {
      margin: 0;
      color: #1f2937;
      font-size: 18px;
      font-weight: 600;
    }

    .close-btn {
      background: none;
      border: none;
      font-size: 24px;
      color: #6b7280;
      cursor: pointer;
      padding: 0;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      transition: all 0.2s;
    }

    .close-btn:hover {
      background-color: #f3f4f6;
      color: #1f2937;
    }

    .dialog-body {
      padding: 20px;
      color: #4b5563;
      line-height: 1.6;
    }

    .dialog-body p {
      margin: 0;
    }

    .dialog-footer {
      display: flex;
      gap: 12px;
      padding: 16px 20px;
      border-top: 1px solid #e5e7eb;
      justify-content: flex-end;
    }

    .btn {
      padding: 10px 20px;
      border-radius: 8px;
      border: none;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 14px;
    }

    .btn-secondary {
      background-color: #e5e7eb;
      color: #1f2937;
    }

    .btn-secondary:hover {
      background-color: #d1d5db;
    }

    .btn-primary {
      background-color: #3b82f6;
      color: white;
    }

    .btn-primary:hover {
      background-color: #2563eb;
    }

    @media (max-width: 512px) {
      .dialog-box {
        max-width: 95%;
      }

      .dialog-header {
        padding: 16px;
      }

      .dialog-body {
        padding: 16px;
      }

      .dialog-footer {
        padding: 12px 16px;
      }
    }
  `]
})
export class DialogComponent implements OnInit {
  dialog: DialogState | null = null;

  constructor(private dialogService: DialogService) {}

  ngOnInit(): void {
    this.dialogService.dialog$.subscribe((state: DialogState) => {
      this.dialog = state;
    });
  }

  onConfirm(): void {
    this.dialogService.close(true);
  }

  onCancel(): void {
    this.dialogService.close(false);
  }
}
