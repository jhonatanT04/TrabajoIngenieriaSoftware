import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

/**
 * Componente Navbar
 * Barra de navegación superior
 */
@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <nav class="navbar">
      <div class="navbar-brand">
        <img *ngIf="logo" [src]="logo" alt="Logo" class="logo">
        <span class="app-name">{{ appName }}</span>
      </div>

      <div class="navbar-menu">
        <button class="menu-toggle" (click)="toggleSidebar.emit()" *ngIf="showMenuToggle">
          <span class="material-icons">menu</span>
        </button>

        <div class="navbar-actions">
          <button class="nav-button" *ngIf="showNotifications" (click)="onNotifications()">
            <span class="material-icons">notifications</span>
            <span class="badge" *ngIf="notificationCount > 0">{{ notificationCount }}</span>
          </button>

          <div class="user-menu">
            <button class="user-button" (click)="toggleUserMenu()">
              <img *ngIf="userAvatar" [src]="userAvatar" alt="Usuario" class="user-avatar">
              <span class="material-icons" *ngIf="!userAvatar">account_circle</span>
              <span class="user-name">{{ userName }}</span>
              <span class="material-icons">arrow_drop_down</span>
            </button>

            <div class="dropdown-menu" *ngIf="showDropdown">
              <a routerLink="/perfil" class="dropdown-item">
                <span class="material-icons">person</span>
                Mi Perfil
              </a>
              <a routerLink="/configuracion" class="dropdown-item">
                <span class="material-icons">settings</span>
                Configuración
              </a>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item" (click)="onLogout()">
                <span class="material-icons">logout</span>
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  `,
  styles: [`
    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background-color: #1976d2;
      color: white;
      padding: 0 1.5rem;
      height: 64px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      position: sticky;
      top: 0;
      z-index: 1000;
    }

    .navbar-brand {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .logo {
      height: 40px;
      width: auto;
    }

    .app-name {
      font-size: 1.25rem;
      font-weight: 600;
    }

    .navbar-menu {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .menu-toggle {
      background: none;
      border: none;
      color: white;
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 4px;
      display: flex;
      align-items: center;
    }

    .menu-toggle:hover {
      background-color: rgba(255,255,255,0.1);
    }

    .navbar-actions {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .nav-button {
      position: relative;
      background: none;
      border: none;
      color: white;
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 4px;
      display: flex;
      align-items: center;
    }

    .nav-button:hover {
      background-color: rgba(255,255,255,0.1);
    }

    .badge {
      position: absolute;
      top: 4px;
      right: 4px;
      background-color: #f44336;
      color: white;
      border-radius: 10px;
      padding: 2px 6px;
      font-size: 0.75rem;
      font-weight: bold;
    }

    .user-menu {
      position: relative;
    }

    .user-button {
      background: none;
      border: none;
      color: white;
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .user-button:hover {
      background-color: rgba(255,255,255,0.1);
    }

    .user-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      object-fit: cover;
    }

    .user-name {
      font-size: 0.875rem;
      max-width: 150px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .dropdown-menu {
      position: absolute;
      top: 100%;
      right: 0;
      margin-top: 0.5rem;
      background-color: white;
      border-radius: 4px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      min-width: 200px;
      overflow: hidden;
    }

    .dropdown-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1rem;
      color: #333;
      text-decoration: none;
      border: none;
      background: none;
      width: 100%;
      text-align: left;
      cursor: pointer;
      font-size: 0.875rem;
    }

    .dropdown-item:hover {
      background-color: #f5f5f5;
    }

    .dropdown-item .material-icons {
      font-size: 1.25rem;
      color: #666;
    }

    .dropdown-divider {
      height: 1px;
      background-color: #e0e0e0;
      margin: 0.5rem 0;
    }

    .material-icons {
      font-size: 1.5rem;
    }

    @media (max-width: 768px) {
      .user-name {
        display: none;
      }
    }
  `]
})
export class NavbarComponent {
  @Input() appName = 'App';
  @Input() logo = '';
  @Input() userName = 'Usuario';
  @Input() userAvatar = '';
  @Input() showMenuToggle = true;
  @Input() showNotifications = true;
  @Input() notificationCount = 0;

  @Output() toggleSidebar = new EventEmitter<void>();
  @Output() logout = new EventEmitter<void>();
  @Output() notifications = new EventEmitter<void>();

  showDropdown = false;

  toggleUserMenu() {
    this.showDropdown = !this.showDropdown;
  }

  onLogout() {
    this.showDropdown = false;
    this.logout.emit();
  }

  onNotifications() {
    this.notifications.emit();
  }
}
