import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface DialogConfig {
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
}

export interface DialogState extends DialogConfig {
  isOpen: boolean;
  resolveCallback?: (value: boolean) => void;
}

@Injectable({
  providedIn: 'root'
})
export class DialogService {
  private dialogState = new BehaviorSubject<DialogState>({
    title: '',
    message: '',
    confirmText: 'Aceptar',
    cancelText: 'Cancelar',
    isOpen: false
  });

  public dialog$ = this.dialogState.asObservable();

  confirm(config: DialogConfig): Promise<boolean> {
    return new Promise((resolve) => {
      this.dialogState.next({
        ...config,
        confirmText: config.confirmText || 'Aceptar',
        cancelText: config.cancelText || 'Cancelar',
        isOpen: true,
        resolveCallback: resolve
      });
    });
  }

  close(result: boolean): void {
    const state = this.dialogState.value;
    if (state.resolveCallback) {
      state.resolveCallback(result);
    }
    this.dialogState.next({
      title: '',
      message: '',
      confirmText: 'Aceptar',
      cancelText: 'Cancelar',
      isOpen: false
    });
  }
}
