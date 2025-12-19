import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ClientesService, Cliente } from '../../core/services/clientes.service';

@Component({
  standalone: true,
  selector: 'app-cliente-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './cliente-list.component.html'
})
export class ClienteListComponent implements OnInit {

  clientes: Cliente[] = [];

  constructor(private service: ClientesService) {}

  ngOnInit(): void {
    this.clientes = this.service.getAll();
  }
}
