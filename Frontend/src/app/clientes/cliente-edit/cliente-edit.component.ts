import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ClienteService } from '../../core/services/cliente.service';

@Component({
  standalone: true,
  selector: 'app-cliente-edit',
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule],
  templateUrl: './cliente-edit.component.html',
  styleUrls: ['./cliente-edit.component.css']
})
export class ClienteEditComponent implements OnInit {
  cliente: any;
  editForm!: FormGroup;
  loading = false;
  error = '';
  successMessage = '';
  clienteId: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private clienteService: ClienteService,
    private fb: FormBuilder
  ) {
    this.initForm();
  }

  ngOnInit(): void {
    this.clienteId = this.route.snapshot.paramMap.get('id');
    if (!this.clienteId) {
      this.error = 'ID de cliente no válido';
      return;
    }
    this.loadCliente();
  }

  initForm(): void {
    this.editForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      document_type: ['', Validators.required],
      document_number: ['', Validators.required],
      email: ['', [Validators.email]],
      phone: [''],
      preferred_contact_method: [''],
      address: [''],
      city: [''],
      segment: ['', Validators.required],
      is_active: [true],
      loyalty_points: [0],
      notes: [''],
      business_name: ['']
    });
  }

  loadCliente(): void {
    if (!this.clienteId) return;
    this.loading = true;
    this.clienteService.getById(this.clienteId).subscribe({
      next: (cliente) => {
        this.cliente = cliente;
        this.editForm.patchValue(cliente);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando cliente:', err);
        this.error = 'Error al cargar el cliente';
        this.loading = false;
      }
    });
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.editForm.get(fieldName);
    return !!(field && field.invalid && (field.dirty || field.touched));
  }

  isFormValid(): boolean {
    return this.editForm.valid;
  }

  guardar(): void {
    if (!this.editForm.valid || !this.clienteId) {
      this.error = 'Por favor completa los campos requeridos';
      return;
    }

    this.loading = true;
    this.error = '';
    this.successMessage = '';

    const formData = this.editForm.value;

    this.clienteService.update(this.clienteId, formData).subscribe({
      next: (response) => {
        this.successMessage = 'Cliente actualizado exitosamente';
        this.loading = false;
        setTimeout(() => {
          this.router.navigate(['/clientes', this.clienteId]);
        }, 1500);
      },
      error: (err) => {
        console.error('Error actualizando cliente:', err);
        this.error = 'Error al actualizar el cliente';
        this.loading = false;
      }
    });
  }
}
