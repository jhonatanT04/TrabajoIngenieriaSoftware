import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { InventarioService } from '../../../core/services/inventario.service';

@Component({
  standalone: true,
  selector: 'app-stock-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './stock-list.component.html'
})
export class StockListComponent implements OnInit {

  productos: any[] = [];

  constructor(private inventario: InventarioService) {}

  ngOnInit() {
    this.productos = this.inventario.getProductos();
  }
}
