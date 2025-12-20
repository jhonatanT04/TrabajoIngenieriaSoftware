import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

export interface MenuItem {
  label: string;
  icon: string;
  route?: string;
  children?: MenuItem[];
  badge?: string;
  divider?: boolean;
}

/**
 * Componente Sidebar
 * Menú lateral de navegación
 */
@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <aside class="sidebar" [class.collapsed]="collapsed">
      <div class="sidebar-header">
        <h3 *ngIf="!collapsed">{{ title }}</h3>
        <button class="collapse-toggle" (click)="toggleCollapse()">
          <span class="material-icons">{{ collapsed ? 'chevron_right' : 'chevron_left' }}</span>
        </button>
      </div>

      <nav class="sidebar-menu">
        <div *ngFor="let item of menuItems" class="menu-item-wrapper">
          <div *ngIf="item.divider" class="menu-divider"></div>

          <a *ngIf="item.route && !item.children"
             [routerLink]="item.route"
             routerLinkActive="active"
             class="menu-item"
             [title]="collapsed ? item.label : ''">
            <span class="material-icons">{{ item.icon }}</span>
            <span class="menu-label" *ngIf="!collapsed">{{ item.label }}</span>
            <span class="menu-badge" *ngIf="item.badge && !collapsed">{{ item.badge }}</span>
          </a>

          <div *ngIf="item.children" class="menu-item-group">
            <button class="menu-item"
                    (click)="toggleSubmenu(item)"
                    [class.active]="isSubmenuOpen(item)"
                    [title]="collapsed ? item.label : ''">
              <span class="material-icons">{{ item.icon }}</span>
              <span class="menu-label" *ngIf="!collapsed">{{ item.label }}</span>
              <span class="material-icons expand-icon" *ngIf="!collapsed">
                {{ isSubmenuOpen(item) ? 'expand_less' : 'expand_more' }}
              </span>
            </button>

            <div class="submenu" *ngIf="isSubmenuOpen(item) && !collapsed">
              <a *ngFor="let child of item.children"
                 [routerLink]="child.route"
                 routerLinkActive="active"
                 class="submenu-item">
                <span class="material-icons">{{ child.icon }}</span>
                <span class="menu-label">{{ child.label }}</span>
              </a>
            </div>
          </div>
        </div>
      </nav>
    </aside>
  `,
  styles: [`
    .sidebar {
      width: 260px;
      height: calc(100vh - 64px);
      background-color: #2c3e50;
      color: white;
      transition: width 0.3s ease;
      overflow-x: hidden;
      overflow-y: auto;
      position: sticky;
      top: 64px;
    }

    .sidebar.collapsed {
      width: 64px;
    }

    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .sidebar-header h3 {
      margin: 0;
      font-size: 1.125rem;
      font-weight: 600;
    }

    .collapse-toggle {
      background: none;
      border: none;
      color: white;
      cursor: pointer;
      padding: 0.25rem;
      border-radius: 4px;
      display: flex;
      align-items: center;
    }

    .collapse-toggle:hover {
      background-color: rgba(255,255,255,0.1);
    }

    .sidebar-menu {
      padding: 0.5rem 0;
    }

    .menu-divider {
      height: 1px;
      background-color: rgba(255,255,255,0.1);
      margin: 0.5rem 0;
    }

    .menu-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.875rem 1rem;
      color: rgba(255,255,255,0.8);
      text-decoration: none;
      border: none;
      background: none;
      width: 100%;
      text-align: left;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
    }

    .menu-item:hover {
      background-color: rgba(255,255,255,0.1);
      color: white;
    }

    .menu-item.active {
      background-color: rgba(255,255,255,0.15);
      color: white;
      border-left: 3px solid #3498db;
    }

    .menu-item .material-icons {
      font-size: 1.5rem;
      min-width: 24px;
    }

    .menu-label {
      flex: 1;
      font-size: 0.875rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .menu-badge {
      background-color: #e74c3c;
      color: white;
      border-radius: 10px;
      padding: 2px 8px;
      font-size: 0.75rem;
      font-weight: bold;
    }

    .expand-icon {
      font-size: 1.25rem;
    }

    .submenu {
      background-color: rgba(0,0,0,0.2);
      padding: 0.25rem 0;
    }

    .submenu-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1rem 0.75rem 3rem;
      color: rgba(255,255,255,0.7);
      text-decoration: none;
      transition: all 0.2s;
      font-size: 0.875rem;
    }

    .submenu-item:hover {
      background-color: rgba(255,255,255,0.1);
      color: white;
    }

    .submenu-item.active {
      background-color: rgba(255,255,255,0.15);
      color: white;
    }

    .submenu-item .material-icons {
      font-size: 1.25rem;
      min-width: 20px;
    }

    ::-webkit-scrollbar {
      width: 8px;
    }

    ::-webkit-scrollbar-track {
      background: rgba(0,0,0,0.1);
    }

    ::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0.2);
      border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: rgba(255,255,255,0.3);
    }
  `]
})
export class SidebarComponent {
  @Input() title = 'Menú';
  @Input() menuItems: MenuItem[] = [];
  @Input() collapsed = false;

  @Output() collapsedChange = new EventEmitter<boolean>();

  private openSubmenus = new Set<MenuItem>();

  toggleCollapse() {
    this.collapsed = !this.collapsed;
    this.collapsedChange.emit(this.collapsed);

    if (this.collapsed) {
      this.openSubmenus.clear();
    }
  }

  toggleSubmenu(item: MenuItem) {
    if (this.openSubmenus.has(item)) {
      this.openSubmenus.delete(item);
    } else {
      this.openSubmenus.add(item);
    }
  }

  isSubmenuOpen(item: MenuItem): boolean {
    return this.openSubmenus.has(item);
  }
}
