import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ParametrosService {
  impuesto = 0.12;
  moneda = 'USD';
  descuentoGlobal = 0;

  setImpuesto(v: number) { this.impuesto = v; }
  setMoneda(v: string) { this.moneda = v; }
  setDescuento(v: number) { this.descuentoGlobal = v; }
}
