import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface TableColumn {
  key: string;
  label: string;
  sortable?: boolean;
  type?: 'text' | 'number' | 'date' | 'boolean' | 'badge' | 'actions';
  format?: (value: any) => string;
}

/**
 * Componente Table
 * Tabla de datos reutilizable con ordenamiento y paginación
 */
@Component({
  selector: 'app-table',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th *ngFor="let column of columns"
                [class.sortable]="column.sortable"
                (click)="column.sortable && onSort(column.key)">
              {{ column.label }}
              <span class="sort-icon" *ngIf="column.sortable">
                <span class="material-icons" *ngIf="sortColumn === column.key">
                  {{ sortDirection === 'asc' ? 'arrow_upward' : 'arrow_downward' }}
                </span>
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let row of paginatedData"
              [class.selectable]="selectable"
              (click)="onRowClick(row)">
            <td *ngFor="let column of columns" [class]="'type-' + (column.type || 'text')">
              <ng-container [ngSwitch]="column.type">
                <span *ngSwitchCase="'date'">
                  {{ formatDate(row[column.key]) }}
                </span>
                <span *ngSwitchCase="'boolean'">
                  <span class="badge" [class.badge-success]="row[column.key]"
                        [class.badge-danger]="!row[column.key]">
                    {{ row[column.key] ? 'Sí' : 'No' }}
                  </span>
                </span>
                <span *ngSwitchCase="'badge'" [class]="'badge ' + getBadgeClass(row[column.key])">
                  {{ row[column.key] }}
                </span>
                <span *ngSwitchDefault>
                  {{ column.format ? column.format(row[column.key]) : row[column.key] }}
                </span>
              </ng-container>
            </td>
          </tr>
          <tr *ngIf="!data || data.length === 0">
            <td [attr.colspan]="columns.length" class="empty-state">
              {{ emptyMessage }}
            </td>
          </tr>
        </tbody>
      </table>

      <div class="table-footer" *ngIf="pagination && data.length > 0">
        <div class="pagination-info">
          Mostrando {{ startIndex + 1 }} - {{ endIndex }} de {{ data.length }} registros
        </div>
        <div class="pagination-controls">
          <button class="pagination-btn"
                  (click)="previousPage()"
                  [disabled]="currentPage === 1">
            <span class="material-icons">chevron_left</span>
          </button>
          <span class="page-info">Página {{ currentPage }} de {{ totalPages }}</span>
          <button class="pagination-btn"
                  (click)="nextPage()"
                  [disabled]="currentPage === totalPages">
            <span class="material-icons">chevron_right</span>
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .table-container {
      background-color: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow: hidden;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
    }

    thead {
      background-color: #f5f5f5;
      border-bottom: 2px solid #e0e0e0;
    }

    th {
      padding: 1rem;
      text-align: left;
      font-weight: 600;
      color: #333;
      font-size: 0.875rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    th.sortable {
      cursor: pointer;
      user-select: none;
    }

    th.sortable:hover {
      background-color: #eeeeee;
    }

    .sort-icon {
      display: inline-flex;
      vertical-align: middle;
      margin-left: 0.25rem;
    }

    .sort-icon .material-icons {
      font-size: 1.25rem;
    }

    tbody tr {
      border-bottom: 1px solid #e0e0e0;
      transition: background-color 0.2s;
    }

    tbody tr:hover {
      background-color: #f9f9f9;
    }

    tbody tr.selectable {
      cursor: pointer;
    }

    td {
      padding: 1rem;
      color: #666;
      font-size: 0.875rem;
    }

    .empty-state {
      text-align: center;
      padding: 3rem;
      color: #999;
      font-style: italic;
    }

    .badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
    }

    .badge-success {
      background-color: #d4edda;
      color: #155724;
    }

    .badge-danger {
      background-color: #f8d7da;
      color: #721c24;
    }

    .badge-warning {
      background-color: #fff3cd;
      color: #856404;
    }

    .badge-info {
      background-color: #d1ecf1;
      color: #0c5460;
    }

    .table-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background-color: #f9f9f9;
      border-top: 1px solid #e0e0e0;
    }

    .pagination-info {
      font-size: 0.875rem;
      color: #666;
    }

    .pagination-controls {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .pagination-btn {
      background: none;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 0.5rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      color: #333;
    }

    .pagination-btn:hover:not(:disabled) {
      background-color: #f5f5f5;
    }

    .pagination-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .page-info {
      font-size: 0.875rem;
      color: #666;
    }

    .material-icons {
      font-size: 1.25rem;
    }

    @media (max-width: 768px) {
      .table-container {
        overflow-x: auto;
      }

      th, td {
        padding: 0.75rem;
        font-size: 0.8125rem;
      }

      .table-footer {
        flex-direction: column;
        gap: 1rem;
      }
    }
  `]
})
export class TableComponent {
  @Input() columns: TableColumn[] = [];
  @Input() data: any[] = [];
  @Input() pagination = true;
  @Input() pageSize = 10;
  @Input() selectable = false;
  @Input() emptyMessage = 'No hay datos para mostrar';

  @Output() rowClick = new EventEmitter<any>();

  sortColumn = '';
  sortDirection: 'asc' | 'desc' = 'asc';
  currentPage = 1;

  get sortedData() {
    if (!this.sortColumn) {
      return this.data;
    }

    return [...this.data].sort((a, b) => {
      const aVal = a[this.sortColumn];
      const bVal = b[this.sortColumn];

      if (aVal === bVal) return 0;

      const comparison = aVal > bVal ? 1 : -1;
      return this.sortDirection === 'asc' ? comparison : -comparison;
    });
  }

  get paginatedData() {
    if (!this.pagination) {
      return this.sortedData;
    }

    const start = (this.currentPage - 1) * this.pageSize;
    const end = start + this.pageSize;
    return this.sortedData.slice(start, end);
  }

  get totalPages() {
    return Math.ceil(this.data.length / this.pageSize);
  }

  get startIndex() {
    return (this.currentPage - 1) * this.pageSize;
  }

  get endIndex() {
    return Math.min(this.startIndex + this.pageSize, this.data.length);
  }

  onSort(columnKey: string) {
    if (this.sortColumn === columnKey) {
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortColumn = columnKey;
      this.sortDirection = 'asc';
    }
  }

  onRowClick(row: any) {
    if (this.selectable) {
      this.rowClick.emit(row);
    }
  }

  previousPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  formatDate(value: any): string {
    if (!value) return '';
    const date = new Date(value);
    return date.toLocaleDateString('es-ES');
  }

  getBadgeClass(value: string): string {
    // Implementar lógica para determinar la clase del badge según el valor
    const lowerValue = value?.toLowerCase();
    if (lowerValue?.includes('completada') || lowerValue?.includes('activo')) {
      return 'badge-success';
    } else if (lowerValue?.includes('pendiente')) {
      return 'badge-warning';
    } else if (lowerValue?.includes('cancelada') || lowerValue?.includes('inactivo')) {
      return 'badge-danger';
    }
    return 'badge-info';
  }
}
