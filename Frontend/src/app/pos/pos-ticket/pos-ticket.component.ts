import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-pos-ticket',
  imports: [CommonModule],
  templateUrl: './pos-ticket.component.html',
  styleUrls: ['./pos-ticket.component.css']
})
export class PosTicketComponent {

  data = history.state;
  now = new Date();
  folio = Math.floor(Math.random() * 10000).toString().padStart(4, '0');

  constructor(private router: Router) {
    if (!this.data || !this.data.carrito) {
      this.router.navigate(['/pos']);
    }
  }

  nuevaVenta() {
    this.router.navigate(['/pos']);
  }
}
