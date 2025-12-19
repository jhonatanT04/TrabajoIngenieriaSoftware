import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-pos-ticket',
  imports: [CommonModule],
  templateUrl: './pos-ticket.component.html'
})
export class PosTicketComponent {

  data = history.state;

  constructor(private router: Router) {}

  nuevaVenta() {
    this.router.navigate(['/pos']);
  }
}
