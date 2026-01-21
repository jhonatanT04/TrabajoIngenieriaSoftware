import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { UsuariosService } from '../../../core/services/usuarios.service';
import { Usuario, Profile } from '../../../core/models/usuario.model';

@Component({
  standalone: true,
  selector: 'app-usuario-list',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './usuario-list.component.html',
  styleUrls: ['./usuario-list.component.css']
})
export class UsuarioListComponent implements OnInit {

  public usuarios: Usuario[] = [];
  public filtered: Usuario[] = [];
  public searchQuery: string = '';
  public loading: boolean = true;
  public error: string = '';

  constructor(private service: UsuariosService) {}

  ngOnInit(): void {
    this.loadUsuarios();
    this.loadRoles();
    // Microtask para asegurar render en entornos sin zone.js
    setTimeout(() => {
      if (this.loading) this.loadUsuarios();
    }, 0);
  }
      public roles: Profile[] = [];
      public selectedRoleId: string | 'all' = 'all';
      public selectedStatus: 'all' | 'active' | 'inactive' = 'all';
      public showFilters = false;

  loadUsuarios(): void {
    this.loading = true;
    this.service.getAll().subscribe({
      next: (usuarios) => {
        this.usuarios = usuarios;
        this.applyFilter();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando usuarios:', err);
        this.error = 'Error al cargar usuarios. Por favor, intente nuevamente.';
        this.loading = false;
      }
    });
  }

  loadRoles(): void {
    this.service.getProfiles().subscribe({
      next: (profiles) => {
        this.roles = profiles;
      },
      error: () => {
        this.roles = [
          { id: '1', name: 'Administrador', is_active: true },
          { id: '2', name: 'Cajero', is_active: true },
          { id: '3', name: 'Inventario', is_active: true },
        ];
      }
    });
  }

  onSearch(query: string): void {
    this.searchQuery = query;
    this.applyFilter();
  }

  applyFilter(): void {
    const q = this.searchQuery.trim().toLowerCase();
    const byText = (u: Usuario) => !q || (
      u.username?.toLowerCase().includes(q) ||
      u.email?.toLowerCase().includes(q) ||
      (u.profile?.name || '').toLowerCase().includes(q) ||
      `${u.first_name ?? ''} ${u.last_name ?? ''}`.toLowerCase().includes(q)
    );
    const byRole = (u: Usuario) => this.selectedRoleId === 'all' || (u.profile?.id === this.selectedRoleId);
    const byStatus = (u: Usuario) => this.selectedStatus === 'all' || (this.selectedStatus === 'active' ? u.is_active : !u.is_active);

    this.filtered = this.usuarios.filter(u => byText(u) && byRole(u) && byStatus(u));
  }

      toggleFilters(): void {
        this.showFilters = !this.showFilters;
      }

      clearFilters(): void {
        this.searchQuery = '';
        this.selectedRoleId = 'all';
        this.selectedStatus = 'all';
        this.applyFilter();
  }

  exportCSV(): void {
    const rows = (this.filtered.length ? this.filtered : this.usuarios).map(u => ({
      ID: u.id,
      Usuario: u.username,
      Email: u.email,
      Nombre: `${u.first_name ?? ''} ${u.last_name ?? ''}`.trim(),
      Rol: u.profile?.name ?? '',
      Estado: u.is_active ? 'Activo' : 'Inactivo',
      Creado: u.created_at,
      Actualizado: u.updated_at
    }));

    const headers = ['ID','Usuario','Email','Nombre','Rol','Estado','Creado','Actualizado'];
    const csvRows = rows.map(r => headers
      .map(h => `"${String((r as any)[h] ?? '').replace(/\"/g,'\"\"')}"`)
      .join(','));
    const csv = [headers.join(','), ...csvRows].join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'usuarios.csv';
    a.click();
    URL.revokeObjectURL(url);
  }

  getRoleBadgeClass(role: string): string {
    const roleClasses: { [key: string]: string } = {
      'Administrador': 'badge-danger',
      'Cajero': 'badge-info',
      'Inventario': 'badge-warning',
      'Gerente': 'badge-success',
      'Supervisor': 'badge-primary'
    };
    return roleClasses[role] || 'badge-secondary';
  }

  deleteUsuario(usuario: Usuario): void {
    if (confirm(`¿Estás seguro de desactivar al usuario ${usuario.first_name} ${usuario.last_name}?`)) {
      this.service.delete(usuario.id).subscribe({
        next: () => {
          console.log('Usuario desactivado:', usuario.id);
          this.loadUsuarios();
        },
        error: (err) => {
          console.error('Error desactivando usuario:', err);
          alert('Error al desactivar usuario');
        }
      });
    }
  }
}
