import { Injectable } from '@angular/core';
import { CajaService } from '../../core/services/caja.service';
import { MovimientosService } from '../../core/services/movimientos.service';
import { ClientesService } from '../../core/services/clientes.service';

@Injectable({ providedIn: 'root' })
export class ReportesService {

  constructor(
    private caja: CajaService,
    private movimientos: MovimientosService,
    private clientes: ClientesService
  ) {}

  reporteCaja() {
    return this.caja.getEstado();
  }

  reporteInventario() {
    return this.movimientos.getAll();
  }

  reporteClientes() {
    return this.clientes.getAll();
  }

  reporteVentas() {
    return this.movimientos
      .getAll()
      .filter((m: any) => m.tipo === 'SALIDA');
  }
}
