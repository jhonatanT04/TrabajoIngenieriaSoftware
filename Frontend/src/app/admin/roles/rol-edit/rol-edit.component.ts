import { Component } from '@angular/core';          // 👈 IMPORTAR Component
import { CommonModule } from '@angular/common';    // 👈 IMPORTAR CommonModule

@Component({
  standalone: true,
  selector: 'app-rol-edit',
  imports: [CommonModule],                         // 👈 IMPORTAR MODULES USADOS
  template: `<h2>Editar Rol</h2><p>(Configuración futura)</p>`
})
export class RolEditComponent {}
