// Reporte de Caja Component
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { ReportesService, FiltroReporte } from '../../services/reportes.service';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

@Component({
  standalone: true,
  selector: 'app-reporte-caja',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './reporte-caja.component.html',
  styleUrls: ['./reporte-caja.component.css']
})
export class ReporteCajaComponent implements OnInit {

  sesiones: any[] = [];
  loading = false;
  error = '';
  
  filtro: FiltroReporte = {};

  totalSesiones = 0;
  totalApertura = 0;
  totalCierre = 0;
  totalDiferencia = 0;

  constructor(
    private reportes: ReportesService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarReporte();
  }

  cargarReporte(): void {
    this.loading = true;
    this.error = '';
    this.reportes.reporteCaja(this.filtro).subscribe({
      next: (data) => {
        this.sesiones = Array.isArray(data) ? data : [];
        this.calcularTotales();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar reporte:', err);
        this.error = 'Error al cargar el reporte de caja';
        this.loading = false;
      }
    });
  }

  calcularTotales(): void {
    this.totalSesiones = this.sesiones.length;
    this.totalApertura = 0;
    this.totalCierre = 0;
    this.totalDiferencia = 0;

    this.sesiones.forEach(sesion => {
      this.totalApertura += sesion.opening_amount || 0;
      this.totalCierre += sesion.actual_closing_amount || 0;
      this.totalDiferencia += sesion.difference || 0;
    });
  }

  limpiarFiltros(): void {
    this.filtro = {};
    this.cargarReporte();
  }

  descargarPDF(): void {
    if (!this.sesiones.length) {
      alert('No hay datos para descargar');
      return;
    }
    
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    let y = 20;
    
    // Título
    doc.setFontSize(16);
    doc.text('Reporte de Sesiones de Caja', pageWidth / 2, y, { align: 'center' });
    y += 10;
    
    // Tabla
    const tableData = this.sesiones.map(s => [
      s.id?.toString() || '',
      s.opening_date || '',
      s.closing_date || '',
      `$ ${(s.opening_amount || 0).toFixed(2)}`,
      `$ ${(s.expected_closing_amount || 0).toFixed(2)}`,
      `$ ${(s.actual_closing_amount || 0).toFixed(2)}`,
      `$ ${(s.difference || 0).toFixed(2)}`,
      s.status || ''
    ]);
    
    autoTable(doc, {
      head: [['ID', 'Apertura', 'Cierre', 'Monto Inicial', 'Monto Esperado', 'Monto Real', 'Diferencia', 'Estado']],
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
    doc.text(`Total Apertura: $ ${this.totalApertura.toFixed(2)}`, 20, finalY + 10);
    doc.text(`Total Cierre: $ ${this.totalCierre.toFixed(2)}`, 20, finalY + 16);
    doc.text(`Total Diferencia: S/ ${this.totalDiferencia.toFixed(2)}`, 20, finalY + 22);
    
    doc.save('reporte_caja.pdf');
  }

  volver(): void {
    this.router.navigate(['/reportes']);
  }
}
