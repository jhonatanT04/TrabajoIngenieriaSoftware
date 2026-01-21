import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ClienteService } from '../../core/services/cliente.service';

@Component({
  standalone: true,
  selector: 'app-cliente-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './cliente-detail.component.html'
})
export class ClienteDetailComponent implements OnInit {

  cliente: any;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private service: ClienteService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      this.error = 'ID de cliente no válido';
      this.loading = false;
      return;
    }
    this.service.getById(id).subscribe({
      next: (cliente) => {
        this.cliente = cliente;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando cliente:', err);
        this.error = 'Error al cargar el cliente';
        this.loading = false;
      }
    });
  }
}
