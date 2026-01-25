import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-reportes-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './reportes-list.component.html',
  styleUrls: ['./reportes-list.component.css']
})
export class ReportesListComponent implements OnInit {

  constructor(private router: Router) {}

  ngOnInit(): void {
    // Los reportes se cargan automáticamente al entrar a la página
  }

  seleccionarReporte(tipo: string): void {
    this.router.navigate(['/reportes', tipo]);
  }
}
