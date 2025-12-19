import { Component } from '@angular/core'; // 👈 IMPORTAR Component
import { CommonModule } from '@angular/common'; // 👈 IMPORTAR CommonModule
import { RolesService } from '../../../core/services/roles.service'; // 👈 IMPORTAR RolesService

@Component({
  standalone: true,
  selector: 'app-rol-list',
  imports: [CommonModule],
  templateUrl: './rol-list.component.html'
})
export class RolListComponent {

  roles: string[]; // definir antes de usar

  constructor(private service: RolesService) {
    this.roles = this.service.getAll(); // inicializar aquí
  }
}
