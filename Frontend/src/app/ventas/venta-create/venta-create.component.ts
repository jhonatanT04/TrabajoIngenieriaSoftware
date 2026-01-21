import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { UsuarioService } from '../../core/services/usuario.service';
import { ClienteService } from '../../core/services/cliente.service';
import { ProductoService } from '../../core/services/producto.service';
import { VentaService } from '../../core/services/venta.service';

interface LineaVenta {
  producto_id: string;
  producto_nombre: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
}

@Component({
  standalone: true,
  selector: 'app-venta-create',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './venta-create.component.html',
  styleUrls: ['./venta-create.component.css']
})
export class VentaCreateComponent implements OnInit {
  usuarios: any[] = [];
  clientes: any[] = [];
  productos: any[] = [];
  lineas: LineaVenta[] = [];

  venta = {
    cliente_id: '',
    fecha: new Date().toISOString().slice(0, 10),
    vendedor_id: '',
    estado: 'completada',
    notas: ''
  };

  nuevoProducto = {
    producto_id: '',
    cantidad: 1
  };

  loading = false;
  error = '';

  constructor(
    private usuarioService: UsuarioService,
    private clienteService: ClienteService,
    private productoService: ProductoService,
    private ventaService: VentaService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.usuarioService.getAll().subscribe({
      next: (usuarios) => {
        console.log('✅ Usuarios cargados:', usuarios);
        this.usuarios = usuarios;
      },
      error: (err) => {
        console.error('❌ Error cargando usuarios:', err);
        this.error = 'No se pudieron cargar los vendedores';
      }
    });

    this.clienteService.getAll().subscribe({
      next: (clientes) => {
        console.log('✅ Clientes cargados:', clientes);
        this.clientes = clientes;
      },
      error: (err) => {
        console.error('❌ Error cargando clientes:', err);
        this.error = 'No se pudieron cargar los clientes';
      }
    });

    this.productoService.getAll().subscribe({
      next: (productos) => {
        console.log('✅ Productos cargados:', productos);
        this.productos = productos;
      },
      error: (err) => {
        console.error('❌ Error cargando productos:', err);
        this.error = 'No se pudieron cargar los productos';
      }
    });
  }

  agregarProducto(): void {
    if (!this.nuevoProducto.producto_id || this.nuevoProducto.cantidad <= 0) {
      this.error = 'Selecciona un producto y cantidad válida';
      return;
    }

    const producto = this.productos.find(p => p.id === this.nuevoProducto.producto_id);
    if (!producto) {
      this.error = 'Producto no encontrado';
      return;
    }

    const index = this.lineas.findIndex(l => l.producto_id === this.nuevoProducto.producto_id);
    
    if (index !== -1) {
      // Crear nueva línea con cantidad actualizada (inmutable)
      const lineaActualizada = {
        ...this.lineas[index],
        cantidad: this.lineas[index].cantidad + this.nuevoProducto.cantidad
      };
      lineaActualizada.subtotal = lineaActualizada.cantidad * lineaActualizada.precio_unitario;
      
      // Reemplazar en array inmutablemente
      this.lineas = [
        ...this.lineas.slice(0, index),
        lineaActualizada,
        ...this.lineas.slice(index + 1)
      ];
    } else {
      this.lineas = [...this.lineas, {
        producto_id: producto.id,
        producto_nombre: producto.name,
        cantidad: this.nuevoProducto.cantidad,
        precio_unitario: producto.sale_price || 0,
        subtotal: this.nuevoProducto.cantidad * (producto.sale_price || 0)
      }];
    }

    // Limpiar el formulario
    this.nuevoProducto = { producto_id: '', cantidad: 1 };
    this.error = '';
  }

  eliminarLinea(index: number): void {
    this.lineas = this.lineas.filter((_, i) => i !== index);
  }

  get total(): number {
    return this.lineas.reduce((sum, linea) => sum + linea.subtotal, 0);
  }

  guardar(): void {
    if (!this.venta.cliente_id) {
      this.error = 'Selecciona un cliente';
      return;
    }
    if (!this.venta.vendedor_id) {
      this.error = 'Selecciona un vendedor';
      return;
    }
    if (this.lineas.length === 0) {
      this.error = 'Agrega al menos un producto';
      return;
    }

    this.loading = true;
    const ventaData = {
      customer_id: this.venta.cliente_id,
      user_id: this.venta.vendedor_id,
      sale_date: this.venta.fecha,
      notes: this.venta.notas,
      status: this.venta.estado,
      items: this.lineas.map(l => ({
        product_id: l.producto_id,
        quantity: l.cantidad,
        unit_price: l.precio_unitario,
        discount_percentage: 0,
        tax_rate: 0
      }))
    };

    this.ventaService.create(ventaData as any).subscribe({
      next: (response: any) => {
        console.log('✅ Venta creada:', response);
        console.log('ID de la venta:', response?.id);
        // Esperar un poco para asegurar que se procesa
        setTimeout(() => {
          // Navegar al detalle de la venta creada
          if (response && response.id && response.id !== 'NaN') {
            console.log('🔄 Navegando a detalle de venta:', response.id);
            this.router.navigate(['/ventas/detalle', response.id]);
          } else {
            console.log('⚠️ No hay ID válido, navegando a lista');
            this.router.navigate(['/ventas']);
          }
        }, 500);
      },
      error: (err) => {
        this.error = 'Error al guardar la venta';
        console.error(err);
        this.loading = false;
      }
    });
  }

  cancelar(): void {
    history.back();
  }
}
