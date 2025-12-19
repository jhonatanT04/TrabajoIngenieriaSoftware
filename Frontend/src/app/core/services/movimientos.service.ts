import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class MovimientosService {

  movimientos: any[] = [];

  registrar(tipo: 'ENTRADA' | 'SALIDA', producto: string, cantidad: number) {
    this.movimientos.push({
      fecha: new Date(),
      tipo,
      producto,
      cantidad
    });
  }

  getAll() {
    return this.movimientos;
  }
}
