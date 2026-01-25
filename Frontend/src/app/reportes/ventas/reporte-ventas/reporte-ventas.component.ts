import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { ReportesService, FiltroReporte } from '../../services/reportes.service';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

@Component({
  standalone: true,
  selector: 'app-reporte-ventas',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './reporte-ventas.component.html',
  styleUrls: ['./reporte-ventas.component.css']
})
export class ReporteVentasComponent implements OnInit {
  ventas: any[] = [];
  loading = false;
  error = '';
  
  filtro: FiltroReporte = {
    fecha_inicio: '',
    fecha_fin: ''
  };

  subtotal = 0;
  totalVentas = 0;
  cantidadVentas = 0;

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
    this.reportes.reporteVentas(this.filtro).subscribe({
      next: (data) => {
        this.ventas = Array.isArray(data) ? data : [];
        this.calcularTotales();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar reporte:', err);
        this.error = 'Error al cargar el reporte de ventas';
        this.loading = false;
      }
    });
  }

  calcularTotales(): void {
    this.subtotal = 0;
    this.totalVentas = 0;
    this.cantidadVentas = this.ventas.length;

    this.ventas.forEach(venta => {
      this.subtotal += venta.subtotal || 0;
      this.totalVentas += venta.total_amount || 0;
    });
  }

  limpiarFiltros(): void {
    this.filtro = {
      fecha_inicio: '',
      fecha_fin: ''
    };
    this.cargarReporte();
  }

  descargarPDF(): void {
    if (!this.ventas.length) {
      alert('No hay datos para descargar');
      return;
    }
    
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    let y = 20;
    
    // Título
    doc.setFontSize(16);
    doc.text('Reporte de Ventas', pageWidth / 2, y, { align: 'center' });
    y += 10;
    
    // Filtros
    doc.setFontSize(10);
    if (this.filtro.fecha_inicio) doc.text(`Desde: ${this.filtro.fecha_inicio}`, 20, y);
    y += 5;
    if (this.filtro.fecha_fin) doc.text(`Hasta: ${this.filtro.fecha_fin}`, 20, y);
    y += 10;
    
    // Tabla
    const tableData = this.ventas.map(v => [
      v.sale_number?.toString() || '',
      v.sale_date || '',
      `${v.customer?.first_name} ${v.customer?.last_name}` || '',
      `$ ${(v.subtotal || 0).toFixed(2)}`,
      `$ ${(v.tax_amount || 0).toFixed(2)}`,
      `$ ${(v.total_amount || 0).toFixed(2)}`
    ]);
    
    autoTable(doc, {
      head: [['Número', 'Fecha', 'Cliente', 'Subtotal', 'Impuesto', 'Total']],
      body: tableData,
      startY: y
    });
    
    // Totales
    const finalY = (doc as any).lastAutoTable?.finalY || y + 50;
    doc.setFontSize(11);
    doc.setFont('', 'bold');
    doc.text(`Subtotal: $ ${this.subtotal.toFixed(2)}`, 20, finalY + 10);
    doc.text(`Total: $ ${this.totalVentas.toFixed(2)}`, 20, finalY + 16);
    
    doc.save('reporte_ventas.pdf');
  }

  volver(): void {
    this.router.navigate(['/reportes']);
  }
}
