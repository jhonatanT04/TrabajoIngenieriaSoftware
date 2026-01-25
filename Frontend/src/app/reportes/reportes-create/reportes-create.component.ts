import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';

interface TipoReporte {
  id: string;
  nombre: string;
  descripcion: string;
  ruta: string;
  icono: string;
}

@Component({
  standalone: true,
  selector: 'app-reportes-create',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './reportes-create.component.html',
  styleUrls: ['./reportes-create.component.css']
})
export class ReportesCreateComponent implements OnInit {
  tiposReporte: TipoReporte[] = [
    {
      id: 'ventas',
      nombre: 'Reporte de Ventas',
      descripcion: 'Analiza ventas por fecha, producto, cliente',
      ruta: '/reportes/ventas',
      icono: 'shopping_cart'
    },
    {
      id: 'inventario',
      nombre: 'Reporte de Inventario',
      descripcion: 'Estado del stock y movimientos de inventario',
      ruta: '/reportes/inventario',
      icono: 'inventory_2'
    },
    {
      id: 'caja',
      nombre: 'Reporte de Caja',
      descripcion: 'Sesiones de caja y transacciones',
      ruta: '/reportes/caja',
      icono: 'point_of_sale'
    },
    {
      id: 'clientes',
      nombre: 'Reporte de Clientes',
      descripcion: 'Listado y análisis de clientes',
      ruta: '/reportes/clientes',
      icono: 'people'
    }
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {}

  seleccionarReporte(tipo: TipoReporte): void {
    this.router.navigate([tipo.ruta]);
  }

  volver(): void {
    this.router.navigate(['/reportes']);
  }
}
