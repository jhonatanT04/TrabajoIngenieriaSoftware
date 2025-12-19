import { Injectable } from '@angular/core';
import { MovimientoCaja } from '../../core/models/movimiento-caja.model';

@Injectable({
  providedIn: 'root'
})
export class CajaService {

  private abierta = false;
  private montoInicial = 0;
  private ventas = 0;
  private movimientos: MovimientoCaja[] = [];

  abrirCaja(monto: number) {
    this.abierta = true;
    this.montoInicial = monto;
    this.ventas = 0;
    this.movimientos = [
      {
        fecha: new Date(),
        tipo: 'INGRESO',
        descripcion: 'Apertura de caja',
        monto
      }
    ];
  }

  registrarVenta(monto: number) {
    if (!this.abierta) return;

    this.ventas += monto;
    this.movimientos.push({
      fecha: new Date(),
      tipo: 'INGRESO',
      descripcion: 'Venta POS',
      monto
    });
  }

  registrarEgreso(monto: number, descripcion: string) {
    if (!this.abierta) return;

    this.movimientos.push({
      fecha: new Date(),
      tipo: 'EGRESO',
      descripcion,
      monto
    });
  }

  getMovimientos(): MovimientoCaja[] {
    return this.movimientos;
  }

  getEstado() {
    const ingresos = this.movimientos
      .filter(m => m.tipo === 'INGRESO')
      .reduce((a, m) => a + m.monto, 0);

    const egresos = this.movimientos
      .filter(m => m.tipo === 'EGRESO')
      .reduce((a, m) => a + m.monto, 0);

    return {
      abierta: this.abierta,
      montoInicial: this.montoInicial,
      ventas: this.ventas,
      ingresos,
      egresos,
      total: ingresos - egresos
    };
  }

  cerrarCaja() {
    this.movimientos.push({
      fecha: new Date(),
      tipo: 'EGRESO',
      descripcion: 'Cierre de caja',
      monto: this.getEstado().total
    });

    this.abierta = false;
  }
}
