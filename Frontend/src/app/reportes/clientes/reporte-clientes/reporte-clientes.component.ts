// Reporte de Clientes Component
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { ReportesService, FiltroReporte } from '../../services/reportes.service';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

@Component({
  standalone: true,
  selector: 'app-reporte-clientes',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './reporte-clientes.component.html',
  styleUrls: ['./reporte-clientes.component.css']
})
export class ReporteClientesComponent implements OnInit {
  clientes: any[] = [];
  loading = false;
  error = '';
  
  filtro: FiltroReporte = {};

  totalClientes = 0;
  clientesActivos = 0;
  clientesInactivos = 0;
  totalPuntos = 0;

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
    this.reportes.reporteClientes(this.filtro).subscribe({
      next: (data) => {
        this.clientes = Array.isArray(data) ? data : [];
        this.calcularTotales();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar reporte:', err);
        this.error = 'Error al cargar el reporte de clientes';
        this.loading = false;
      }
    });
  }

  calcularTotales(): void {
    this.totalClientes = this.clientes.length;
    this.clientesActivos = this.clientes.filter(c => c.is_active).length;
    this.clientesInactivos = this.clientes.filter(c => !c.is_active).length;
    this.totalPuntos = this.clientes.reduce((sum, c) => sum + (c.loyalty_points || 0), 0);
  }

  limpiarFiltros(): void {
    this.filtro = {};
    this.cargarReporte();
  }

  descargarPDF(): void {
    if (!this.clientes.length) {
      alert('No hay datos para descargar');
      return;
    }
    
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    let y = 20;
    
    // Título
    doc.setFontSize(16);
    doc.text('Reporte de Clientes', pageWidth / 2, y, { align: 'center' });
    y += 10;
    
    // Tabla
    const tableData = this.clientes.map(c => [
      c.document_number || '',
      `${c.first_name} ${c.last_name}` || '',
      c.email || '',
      c.phone || '',
      c.address || '',
      c.loyalty_points?.toString() || '',
      c.is_active ? 'Activo' : 'Inactivo'
    ]);
    
    autoTable(doc, {
      head: [['Documento', 'Nombre', 'Email', 'Teléfono', 'Dirección', 'Puntos', 'Estado']],
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
    doc.text(`Total Clientes: ${this.clientes.length}`, 20, finalY + 10);
    doc.text(`Activos: ${this.clientesActivos}`, 20, finalY + 16);
    doc.text(`Inactivos: ${this.clientesInactivos}`, 20, finalY + 22);
    
    doc.save('reporte_clientes.pdf');
  }

  volver(): void {
    this.router.navigate(['/reportes']);
  }
}
