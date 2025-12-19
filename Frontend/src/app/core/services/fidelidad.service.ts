import { Injectable } from '@angular/core';
import { ClientesService } from './clientes.service';

@Injectable({ providedIn: 'root' })
export class FidelidadService {

  constructor(private clientesService: ClientesService) {}

  sumarPuntos(clienteId: number, monto: number) {
    const cliente = this.clientesService.getById(clienteId);
    if (cliente) {
      cliente.puntos += Math.floor(monto); // 1 punto por dólar
    }
  }

  canjear(clienteId: number, puntos: number) {
    const cliente = this.clientesService.getById(clienteId);
    if (cliente && cliente.puntos >= puntos) {
      cliente.puntos -= puntos;
    }
  }
}
