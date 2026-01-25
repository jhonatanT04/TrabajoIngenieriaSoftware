import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { ReportesService, FiltroReporte } from '../../services/reportes.service';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

@Component({
  standalone: true,
  selector: 'app-reporte-inventario',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './reporte-inventario.component.html',
  styleUrls: ['./reporte-inventario.component.css']
})
export class ReporteInventarioComponent implements OnInit {
  movimientos: any[] = [];
  loading = false;
  error = '';
  
  filtro: FiltroReporte = {};

  totalMovimientos = 0;
  totalEntradas = 0;
  totalSalidas = 0;

  constructor(
    private reportes: ReportesService,
    private router: Router
  ) {}

  ngOnInit() {
    this.cargarReporte();
  }

  cargarReporte(): void {
    this.loading = true;
    this.error = '';
    this.reportes.reporteInventario(this.filtro).subscribe({
      next: (data) => {
        this.movimientos = Array.isArray(data) ? data : [];
        this.calcularTotales();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar reporte:', err);
        this.error = 'Error al cargar el reporte de inventario';
        this.loading = false;
      }
    });
  }

  calcularTotales(): void {
    this.totalMovimientos = this.movimientos.length;
    this.totalEntradas = this.movimientos.filter(m => m.movement_type === 'entrada').length;
    this.totalSalidas = this.movimientos.filter(m => m.movement_type === 'salida').length;
  }

  limpiarFiltros(): void {
    this.filtro = {};
    this.cargarReporte();
  }

  descargarPDF(): void {
    if (!this.movimientos.length) {
      alert('No hay datos para descargar');
      return;
    }
    
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    let y = 20;
    
    // Título
    doc.setFontSize(16);
    doc.text('Reporte de Movimientos de Inventario', pageWidth / 2, y, { align: 'center' });
    y += 10;
    
    // Tabla
    const tableData = this.movimientos.map(m => [
      m.product?.name || '',
      m.movement_type || '',
      m.quantity_moved?.toString() || '',
      m.old_stock?.toString() || '',
      m.new_stock?.toString() || '',
      `$ ${(m.unit_cost || 0).toFixed(2)}`,
      `$ ${(m.total_cost || 0).toFixed(2)}`
    ]);
    
    autoTable(doc, {
      head: [['Producto', 'Tipo', 'Cantidad', 'Stock Anterior', 'Stock Nuevo', 'Precio Unitario', 'Total']],
      body: tableData,
      startY: y,
      didDrawPage: (data: any) => {
        const pageCount = (doc as any).internal.getNumberOfPages();
        const pageSize = doc.internal.pageSize;
        const pageHeight = pageSize.getHeight();
        const pageWidth = pageSize.getWidth();
        doc.setFontSize(10);
        doc.text(`Página ${data.pageNumber} de ${pageCount}`, pageWidth / 2, pageHeight - 10, { align: 'center' });
      }
    });
    
    // Totales
    const finalY = (doc as any).lastAutoTable?.finalY || y + 50;
    doc.setFontSize(11);
    doc.setFont('', 'bold');
    doc.text(`Total Entradas: ${this.totalEntradas}`, 20, finalY + 10);
    doc.text(`Total Salidas: ${this.totalSalidas}`, 20, finalY + 16);
    
    doc.save('reporte_inventario.pdf');
  }

  volver(): void {
    this.router.navigate(['/reportes']);
  }
}
