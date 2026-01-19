import { Injectable } from '@angular/core';
import { CajaService } from '../../core/services/caja.service';
import { InventarioService } from '../../core/services/inventario.service';
import { ClienteService } from '../../core/services/cliente.service';
import { VentaService } from '../../core/services/venta.service';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ReportesService {

  constructor(
    private caja: CajaService,
    private inventario: InventarioService,
    private clientes: ClienteService,
    private ventas: VentaService
  ) {}

  reporteCaja(): Observable<any> {
    return this.caja.getSessions({ status: 'abierta' });
  }

  reporteInventario(): Observable<any> {
    return this.inventario.getMovements();
  }

  reporteClientes(): Observable<any> {
    return this.clientes.getAll();
  }

  reporteVentas(): Observable<any> {
    return this.ventas.getAll();
  }
}
