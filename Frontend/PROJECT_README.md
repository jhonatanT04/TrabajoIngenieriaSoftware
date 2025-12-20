# Sistema de Gestión de Minimercado - Frontend

## 📋 Descripción

Sistema completo de gestión para minimercados desarrollado en **Angular 20** con una arquitectura modular, escalable y moderna. Incluye gestión de inventario, punto de venta (POS), administración de clientes, reportes, y más.

**Versión:** 1.0.0-beta  
**Framework:** Angular 20.3  
**UI Components:** Angular Material 20  
**Estado:** Beta Funcional

---

## 🚀 Características Principales

### Módulos Implementados

- ✅ **Autenticación** - Login, registro, recuperación de contraseña
- ✅ **Dashboard** - Paneles por rol (Admin, Cajero, Almacén, Contador)
- ✅ **Productos** - CRUD completo, categorías, búsqueda
- ✅ **Inventario** - Control de stock, recepciones, movimientos, etiquetas
- ✅ **Proveedores** - Gestión de proveedores y órdenes de compra
- ✅ **Ventas** - Historial, detalles, promociones
- ✅ **POS (Punto de Venta)** - Interface optimizada para cajeros
- ✅ **Caja** - Apertura, cierre, arqueo, movimientos
- ✅ **Clientes** - CRUD, programa de fidelidad
- ✅ **Reportes** - Ventas, inventario, caja, clientes, exportación
- ✅ **Administración** - Usuarios, roles, parámetros del sistema

### Características Técnicas

- 🎨 **UI Moderna** - Diseño limpio y profesional con Angular Material
- 🔐 **Seguridad** - Guards, interceptors, autenticación JWT
- 📱 **Responsive** - Adaptable a todos los dispositivos
- 🧩 **Modular** - Arquitectura de módulos independientes
- 🚦 **Lazy Loading** - Carga de módulos bajo demanda
- 📊 **Reactive Forms** - Validaciones robustas
- 🔄 **HTTP Interceptors** - Manejo centralizado de errores y autenticación
- 🎯 **TypeScript** - Tipado fuerte en todo el proyecto

---

## 📁 Estructura del Proyecto

```
Frontend/
├── src/
│   ├── app/
│   │   ├── core/                    # Funcionalidad central
│   │   │   ├── guards/              # Protección de rutas
│   │   │   │   ├── auth.guard.ts
│   │   │   │   └── role.guard.ts
│   │   │   ├── interceptors/        # HTTP Interceptors
│   │   │   │   ├── auth.interceptor.ts
│   │   │   │   ├── error.interceptor.ts
│   │   │   │   └── loading.interceptor.ts
│   │   │   ├── models/              # Interfaces TypeScript
│   │   │   │   ├── usuario.model.ts
│   │   │   │   ├── producto.model.ts
│   │   │   │   ├── venta.model.ts
│   │   │   │   ├── caja.model.ts
│   │   │   │   ├── inventario.model.ts
│   │   │   │   ├── orden-compra.model.ts
│   │   │   │   ├── reporte.model.ts
│   │   │   │   ├── parametro.model.ts
│   │   │   │   └── index.ts
│   │   │   └── services/            # Servicios REST
│   │   │       ├── auth.service.ts
│   │   │       ├── producto.service.ts
│   │   │       ├── venta.service.ts
│   │   │       ├── cliente.service.ts
│   │   │       ├── caja.service.ts
│   │   │       ├── inventario.service.ts
│   │   │       ├── proveedor.service.ts
│   │   │       ├── usuario.service.ts
│   │   │       ├── reporte.service.ts
│   │   │       ├── parametro.service.ts
│   │   │       └── index.ts
│   │   │
│   │   ├── shared/                  # Componentes reutilizables
│   │   │   ├── components/
│   │   │   │   ├── navbar/
│   │   │   │   ├── sidebar/
│   │   │   │   ├── footer/
│   │   │   │   ├── modal/
│   │   │   │   ├── confirm-dialog/
│   │   │   │   └── table/
│   │   │   ├── pipes/
│   │   │   ├── directives/
│   │   │   └── shared.module.ts
│   │   │
│   │   ├── layout/                  # Layouts principales
│   │   │   ├── admin-layout/        # Layout para administración
│   │   │   ├── pos-layout/          # Layout para punto de venta
│   │   │   └── layout.module.ts
│   │   │
│   │   ├── auth/                    # Autenticación
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   ├── forgot-password/
│   │   │   ├── auth.module.ts
│   │   │   └── auth.routes.ts
│   │   │
│   │   ├── dashboard/               # Dashboards por rol
│   │   │   ├── admin-dashboard/
│   │   │   ├── cajero-dashboard/
│   │   │   ├── almacen-dashboard/
│   │   │   ├── contador-dashboard/
│   │   │   ├── dashboard.module.ts
│   │   │   └── dashboard.routes.ts
│   │   │
│   │   ├── productos/               # Gestión de productos
│   │   │   ├── producto-list/
│   │   │   ├── producto-create/
│   │   │   ├── producto-edit/
│   │   │   ├── producto-detail/
│   │   │   ├── categorias/
│   │   │   ├── productos.module.ts
│   │   │   └── productos.routes.ts
│   │   │
│   │   ├── inventario/              # Gestión de inventario
│   │   │   ├── stock/
│   │   │   ├── recepcion/
│   │   │   ├── movimientos/
│   │   │   ├── etiquetas/
│   │   │   ├── inventario.module.ts
│   │   │   └── inventario.routes.ts
│   │   │
│   │   ├── proveedores/             # Gestión de proveedores
│   │   │   ├── proveedor-list/
│   │   │   ├── proveedor-create/
│   │   │   ├── proveedor-edit/
│   │   │   ├── proveedor-detail/
│   │   │   ├── ordenes-compra/
│   │   │   ├── proveedores.module.ts
│   │   │   └── proveedores.routes.ts
│   │   │
│   │   ├── ventas/                  # Gestión de ventas
│   │   │   ├── venta-list/
│   │   │   ├── venta-detail/
│   │   │   ├── promociones/
│   │   │   ├── ventas.module.ts
│   │   │   └── ventas.routes.ts
│   │   │
│   │   ├── pos/                     # Punto de Venta
│   │   │   ├── pos-home/
│   │   │   ├── pos-carrito/
│   │   │   ├── pos-pago/
│   │   │   ├── pos-ticket/
│   │   │   ├── pos-offline/
│   │   │   ├── pos.module.ts
│   │   │   └── pos.routes.ts
│   │   │
│   │   ├── caja/                    # Gestión de caja
│   │   │   ├── apertura/
│   │   │   ├── cierre/
│   │   │   ├── arqueo/
│   │   │   ├── movimientos/
│   │   │   ├── caja.module.ts
│   │   │   └── caja.routes.ts
│   │   │
│   │   ├── clientes/                # Gestión de clientes
│   │   │   ├── cliente-list/
│   │   │   ├── cliente-create/
│   │   │   ├── cliente-edit/
│   │   │   ├── cliente-detail/
│   │   │   ├── fidelidad/
│   │   │   ├── clientes.module.ts
│   │   │   └── clientes.routes.ts
│   │   │
│   │   ├── reportes/                # Sistema de reportes
│   │   │   ├── inventario/
│   │   │   ├── ventas/
│   │   │   ├── caja/
│   │   │   ├── clientes/
│   │   │   ├── exportacion/
│   │   │   ├── reportes.module.ts
│   │   │   └── reportes.routes.ts
│   │   │
│   │   ├── admin/                   # Administración del sistema
│   │   │   ├── usuarios/
│   │   │   ├── roles/
│   │   │   ├── parametros/
│   │   │   ├── admin.module.ts
│   │   │   └── admin.routes.ts
│   │   │
│   │   ├── not-found/               # Página 404
│   │   │   └── not-found.component.ts
│   │   │
│   │   ├── app.config.ts            # Configuración de la app
│   │   ├── app.routes.ts            # Rutas principales
│   │   └── app.ts                   # Componente raíz
│   │
│   ├── assets/                      # Recursos estáticos
│   │   ├── icons/
│   │   ├── images/
│   │   └── styles/
│   │
│   ├── environments/                # Configuración de ambientes
│   │   ├── environment.ts           # Desarrollo
│   │   └── environment.prod.ts      # Producción
│   │
│   ├── index.html
│   ├── main.ts
│   └── styles.css                   # Estilos globales
│
├── angular.json                     # Configuración de Angular
├── package.json                     # Dependencias
├── tsconfig.json                    # Configuración TypeScript
└── README.md                        # Este archivo
```

---

## 🛠️ Instalación y Configuración

### Requisitos Previos

- **Node.js**: v18.x o superior
- **npm**: v9.x o superior
- **Angular CLI**: v20.x

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno**
   
   Editar `src/environments/environment.ts`:
   ```typescript
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:8000/api',  // URL del backend
     appName: 'Sistema de Gestión de Minimercado',
     version: '1.0.0-beta'
   };
   ```

4. **Iniciar el servidor de desarrollo**
   ```bash
   npm start
   # o
   ng serve
   ```

5. **Abrir en el navegador**
   ```
   http://localhost:4200
   ```

---

## 🔧 Scripts Disponibles

```bash
npm start          # Inicia el servidor de desarrollo
npm run build      # Compila para producción
npm test           # Ejecuta las pruebas unitarias
npm run watch      # Compila en modo watch
```

---

## 🔐 Autenticación y Autorización

### Sistema de Roles

El sistema maneja 4 roles principales:

| Rol | Permisos | Rutas Accesibles |
|-----|----------|------------------|
| **Admin** | Acceso total | Todos los módulos |
| **Cajero** | Ventas y caja | POS, Ventas, Caja, Clientes |
| **Almacén** | Inventario | Productos, Inventario, Proveedores |
| **Contador** | Reportes | Reportes, Dashboard |

### Guards Implementados

- **authGuard**: Verifica autenticación del usuario
- **roleGuard**: Verifica permisos según rol

### Interceptors

- **authInterceptor**: Agrega token JWT a las peticiones
- **errorInterceptor**: Manejo centralizado de errores HTTP
- **loadingInterceptor**: Control de estado de carga global

---

## 🎨 Componentes Compartidos

### Navbar
Barra de navegación superior con:
- Logo y nombre de la aplicación
- Menú de usuario
- Notificaciones
- Toggle del sidebar

### Sidebar
Menú lateral con:
- Navegación jerárquica
- Items expandibles
- Iconos Material
- Modo colapsado

### Footer
Pie de página con información del sistema

### Modal
Modal reutilizable con:
- Tamaños configurables (sm, md, lg, xl)
- Cierre por overlay
- Footer personalizable

### ConfirmDialog
Diálogo de confirmación para acciones críticas con tipos:
- warning
- danger
- info
- success

### Table
Tabla de datos con:
- Ordenamiento por columnas
- Paginación
- Formatos personalizados
- Badges y estados

---

## 📡 Servicios REST

Todos los servicios están configurados para consumir el backend REST:

### Ejemplo de Uso

```typescript
import { ProductoService } from '@core/services';

constructor(private productoService: ProductoService) {}

// Obtener todos los productos
this.productoService.getAll().subscribe(productos => {
  console.log(productos);
});

// Buscar producto
this.productoService.getById(1).subscribe(producto => {
  console.log(producto);
});

// Crear producto
this.productoService.create(nuevoProducto).subscribe(producto => {
  console.log('Producto creado:', producto);
});
```

### Servicios Disponibles

- `AuthService` - Autenticación y sesión
- `ProductoService` - Gestión de productos
- `VentaService` - Operaciones de venta
- `ClienteService` - Gestión de clientes
- `CajaService` - Operaciones de caja
- `InventarioService` - Control de inventario
- `ProveedorService` - Gestión de proveedores
- `UsuarioService` - Administración de usuarios
- `ReporteService` - Generación de reportes
- `ParametroService` - Configuración del sistema

---

## 🧪 Pruebas

### Ejecutar Tests

```bash
npm test
```

### Estructura de Tests

```
src/app/
├── core/
│   └── services/
│       └── producto.service.spec.ts
├── shared/
│   └── components/
│       └── table/table.component.spec.ts
└── productos/
    └── producto-list/producto-list.component.spec.ts
```

---

## 📊 Rutas del Sistema

### Rutas Públicas

| Ruta | Componente | Descripción |
|------|-----------|-------------|
| `/auth/login` | LoginComponent | Inicio de sesión |
| `/auth/register` | RegisterComponent | Registro de usuario |
| `/auth/forgot-password` | ForgotPasswordComponent | Recuperar contraseña |

### Rutas Protegidas (Requieren Auth)

#### Dashboard
- `/dashboard/admin` - Dashboard administrador
- `/dashboard/cajero` - Dashboard cajero
- `/dashboard/almacen` - Dashboard almacén
- `/dashboard/contador` - Dashboard contador

#### Productos
- `/productos/list` - Lista de productos
- `/productos/create` - Crear producto
- `/productos/edit/:id` - Editar producto
- `/productos/detail/:id` - Detalle de producto
- `/productos/categorias` - Gestión de categorías

#### Inventario
- `/inventario/stock` - Control de stock
- `/inventario/recepcion` - Recepciones de mercancía
- `/inventario/movimientos` - Historial de movimientos
- `/inventario/etiquetas` - Generación de etiquetas

#### Proveedores
- `/proveedores/list` - Lista de proveedores
- `/proveedores/create` - Crear proveedor
- `/proveedores/edit/:id` - Editar proveedor
- `/proveedores/detail/:id` - Detalle de proveedor
- `/proveedores/ordenes-compra` - Órdenes de compra

#### Ventas
- `/ventas/list` - Historial de ventas
- `/ventas/detail/:id` - Detalle de venta
- `/ventas/promociones` - Gestión de promociones

#### POS (Solo Cajero)
- `/pos` - Punto de venta principal
- `/pos/carrito` - Carrito de compra
- `/pos/pago` - Proceso de pago
- `/pos/ticket` - Ticket de venta

#### Caja
- `/caja/apertura` - Apertura de caja
- `/caja/cierre` - Cierre de caja
- `/caja/arqueo` - Arqueo de caja
- `/caja/movimientos` - Movimientos de caja

#### Clientes
- `/clientes/list` - Lista de clientes
- `/clientes/create` - Crear cliente
- `/clientes/edit/:id` - Editar cliente
- `/clientes/detail/:id` - Detalle de cliente
- `/clientes/fidelidad` - Programa de fidelidad

#### Reportes
- `/reportes/ventas` - Reporte de ventas
- `/reportes/inventario` - Reporte de inventario
- `/reportes/caja` - Reporte de caja
- `/reportes/clientes` - Reporte de clientes

#### Administración (Solo Admin)
- `/admin/usuarios` - Gestión de usuarios
- `/admin/roles` - Gestión de roles
- `/admin/parametros` - Configuración del sistema

---

## 🎯 Próximas Funcionalidades

- [ ] Modo offline para POS
- [ ] Sincronización de datos
- [ ] Notificaciones push
- [ ] Integración con impresoras térmicas
- [ ] Escaneo de códigos de barras
- [ ] Dashboard analytics avanzado
- [ ] Exportación de reportes a PDF
- [ ] Sistema de backup automático
- [ ] Multi-idioma (i18n)
- [ ] Tema oscuro

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Notas de Desarrollo

### Convenciones de Código

- **Componentes**: PascalCase (ej: `ProductoListComponent`)
- **Servicios**: PascalCase con sufijo Service (ej: `ProductoService`)
- **Interfaces**: PascalCase (ej: `Producto`, `Usuario`)
- **Variables**: camelCase (ej: `productoList`, `currentUser`)
- **Constantes**: UPPER_SNAKE_CASE (ej: `API_URL`)

### Estructura de Componentes

```typescript
@Component({
  selector: 'app-componente',
  standalone: true,
  imports: [],
  templateUrl: './componente.component.html',
  styleUrls: ['./componente.component.css']
})
export class ComponenteComponent {
  // Propiedades
  // Constructor
  // Lifecycle hooks
  // Métodos públicos
  // Métodos privados
}
```

---

## 🐛 Troubleshooting

### Error de CORS
Verificar que el backend esté configurado para aceptar peticiones desde `http://localhost:4200`

### Token expirado
El sistema redirige automáticamente al login cuando el token expira

### Módulo no encontrado
Ejecutar `npm install` para instalar dependencias faltantes

---

## 📄 Licencia

Este proyecto es parte de un trabajo universitario de Ingeniería de Software.

---

## 👥 Equipo de Desarrollo

- Desarrollo Frontend: Angular Team
- Arquitectura: System Architects
- Testing: QA Team

---

## 📞 Soporte

Para soporte y preguntas, contactar al equipo de desarrollo.

---

**Última actualización:** Diciembre 2025  
**Estado:** Beta Funcional  
**Versión:** 1.0.0-beta
