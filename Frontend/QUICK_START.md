# 🚀 Guía Rápida de Inicio - Sistema de Gestión de Minimercado

## ✅ Checklist de Configuración Inicial

### 1. Verificar Instalación

```bash
# Verificar Node.js (debe ser v18+)
node --version

# Verificar npm (debe ser v9+)
npm --version

# Instalar Angular CLI globalmente si no lo tienes
npm install -g @angular/cli@20
```

### 2. Instalar Dependencias

```bash
cd Frontend
npm install
```

### 3. Configurar Backend URL

Editar `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',  // ⬅️ Cambiar a la URL de tu backend
  appName: 'Sistema de Gestión de Minimercado',
  version: '1.0.0-beta'
};
```

### 4. Iniciar Aplicación

```bash
npm start
# La aplicación estará disponible en http://localhost:4200
```

---

## 📂 Estructura de Archivos Creados

### ✅ Core (Funcionalidad Central)

```
core/
├── guards/
│   ├── auth.guard.ts          ✅ Protección de rutas por autenticación
│   └── role.guard.ts          ✅ Protección de rutas por rol
├── interceptors/
│   ├── auth.interceptor.ts    ✅ Agregar token JWT a peticiones
│   ├── error.interceptor.ts   ✅ Manejo centralizado de errores
│   └── loading.interceptor.ts ✅ Control de estado de carga
├── models/                    ✅ Interfaces TypeScript (8 modelos)
│   ├── usuario.model.ts
│   ├── producto.model.ts
│   ├── venta.model.ts
│   ├── caja.model.ts
│   ├── inventario.model.ts
│   ├── orden-compra.model.ts
│   ├── reporte.model.ts
│   └── parametro.model.ts
└── services/                  ✅ Servicios REST (10 servicios)
    ├── auth.service.ts
    ├── producto.service.ts
    ├── venta.service.ts
    ├── cliente.service.ts
    ├── caja.service.ts
    ├── inventario.service.ts
    ├── proveedor.service.ts
    ├── usuario.service.ts
    ├── reporte.service.ts
    └── parametro.service.ts
```

### ✅ Shared (Componentes Reutilizables)

```
shared/
└── components/
    ├── navbar/              ✅ Barra de navegación superior
    ├── sidebar/             ✅ Menú lateral expandible
    ├── footer/              ✅ Pie de página
    ├── modal/               ✅ Modal reutilizable
    ├── confirm-dialog/      ✅ Diálogo de confirmación
    └── table/               ✅ Tabla con ordenamiento y paginación
```

### ✅ Layouts

```
layout/
├── admin-layout/            ✅ Layout para administración
└── pos-layout/              ✅ Layout para punto de venta
```

### ✅ Configuración

```
src/
├── environments/
│   ├── environment.ts       ✅ Configuración desarrollo
│   └── environment.prod.ts  ✅ Configuración producción
├── app.config.ts            ✅ Configuración app (interceptors, providers)
├── app.routes.ts            ✅ Rutas principales con lazy loading
└── styles.css               ✅ Estilos globales
```

---

## 🎯 Próximos Pasos Sugeridos

### Paso 1: Crear Componentes Faltantes

Los módulos ya tienen su estructura base, pero necesitas crear los componentes individuales. Ejemplo:

```bash
# Para crear un componente de lista de productos
ng generate component productos/producto-list --standalone

# Para crear un componente de crear producto
ng generate component productos/producto-create --standalone

# Y así sucesivamente...
```

### Paso 2: Implementar Lógica de Negocio

Cada componente debe:
1. Inyectar el servicio correspondiente
2. Implementar métodos para CRUD
3. Conectar con el backend
4. Manejar errores

**Ejemplo de ProductoListComponent:**

```typescript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductoService } from '../../core/services';
import { Producto } from '../../core/models';
import { TableComponent } from '../../shared/components';

@Component({
  selector: 'app-producto-list',
  standalone: true,
  imports: [CommonModule, TableComponent],
  template: `
    <div class="page-header">
      <h1 class="page-title">Productos</h1>
      <button class="btn btn-primary" (click)="navigateToCreate()">
        <span class="material-icons">add</span>
        Nuevo Producto
      </button>
    </div>

    <app-table
      [columns]="columns"
      [data]="productos"
      [pagination]="true"
      [selectable]="true"
      (rowClick)="onRowClick($event)">
    </app-table>
  `
})
export class ProductoListComponent implements OnInit {
  productos: Producto[] = [];
  columns = [
    { key: 'codigo', label: 'Código', sortable: true },
    { key: 'nombre', label: 'Nombre', sortable: true },
    { key: 'categoria.nombre', label: 'Categoría' },
    { key: 'precio', label: 'Precio', type: 'number' },
    { key: 'stock', label: 'Stock', type: 'number' },
    { key: 'activo', label: 'Estado', type: 'boolean' }
  ];

  constructor(private productoService: ProductoService) {}

  ngOnInit() {
    this.loadProductos();
  }

  loadProductos() {
    this.productoService.getAll().subscribe({
      next: (data) => this.productos = data,
      error: (error) => console.error('Error al cargar productos:', error)
    });
  }

  onRowClick(producto: Producto) {
    // Navegar al detalle o editar
  }

  navigateToCreate() {
    // Navegar a crear producto
  }
}
```

### Paso 3: Configurar Rutas de Cada Módulo

Cada módulo debe tener su archivo `.routes.ts`. Ejemplo para productos:

```typescript
// productos/productos.routes.ts
import { Routes } from '@angular/router';

export const PRODUCTOS_ROUTES: Routes = [
  {
    path: '',
    redirectTo: 'list',
    pathMatch: 'full'
  },
  {
    path: 'list',
    loadComponent: () => import('./producto-list/producto-list.component')
      .then(c => c.ProductoListComponent)
  },
  {
    path: 'create',
    loadComponent: () => import('./producto-create/producto-create.component')
      .then(c => c.ProductoCreateComponent)
  },
  {
    path: 'edit/:id',
    loadComponent: () => import('./producto-edit/producto-edit.component')
      .then(c => c.ProductoEditComponent)
  },
  {
    path: 'detail/:id',
    loadComponent: () => import('./producto-detail/producto-detail.component')
      .then(c => c.ProductoDetailComponent)
  },
  {
    path: 'categorias',
    loadComponent: () => import('./categorias/categorias.component')
      .then(c => c.CategoriasComponent)
  }
];
```

---

## 🔧 Comandos Útiles

```bash
# Generar un componente standalone
ng generate component ruta/nombre --standalone

# Generar un servicio
ng generate service ruta/nombre

# Generar un guard
ng generate guard ruta/nombre --functional

# Generar un interceptor
ng generate interceptor ruta/nombre --functional

# Generar un pipe
ng generate pipe ruta/nombre --standalone

# Compilar para producción
npm run build

# Ejecutar tests
npm test

# Ver el proyecto en modo watch
npm run watch
```

---

## 🎨 Uso de Componentes Compartidos

### Navbar

```typescript
<app-navbar
  [appName]="'Mi App'"
  [userName]="'Usuario'"
  [showNotifications]="true"
  [notificationCount]="5"
  (logout)="onLogout()"
  (toggleSidebar)="toggleSidebar()">
</app-navbar>
```

### Sidebar

```typescript
<app-sidebar
  [title]="'Menú'"
  [menuItems]="menuItems"
  [(collapsed)]="sidebarCollapsed">
</app-sidebar>
```

### Modal

```typescript
<app-modal
  [title]="'Título del Modal'"
  [isOpen]="showModal"
  [size]="'md'"
  (close)="showModal = false">
  <p>Contenido del modal</p>
  <div footer>
    <button class="btn btn-secondary" (click)="showModal = false">Cancelar</button>
    <button class="btn btn-primary" (click)="confirm()">Confirmar</button>
  </div>
</app-modal>
```

### Table

```typescript
<app-table
  [columns]="columns"
  [data]="data"
  [pagination]="true"
  [pageSize]="10"
  [selectable]="true"
  (rowClick)="onRowClick($event)">
</app-table>
```

### Confirm Dialog

```typescript
<app-confirm-dialog
  [isOpen]="showConfirm"
  [title]="'¿Eliminar registro?'"
  [message]="'Esta acción no se puede deshacer'"
  [type]="'danger'"
  [confirmText]="'Eliminar'"
  [cancelText]="'Cancelar'"
  (confirm)="onConfirm()"
  (cancel)="showConfirm = false">
</app-confirm-dialog>
```

---

## 🔐 Autenticación

### Login

```typescript
this.authService.login({ username, password }).subscribe({
  next: (response) => {
    this.authService.setToken(response.access_token);
    this.authService.setCurrentUser(response.usuario);
    this.router.navigate(['/dashboard']);
  },
  error: (error) => {
    console.error('Error de login:', error);
  }
});
```

### Logout

```typescript
this.authService.logout().subscribe(() => {
  this.authService.removeToken();
  this.authService.removeCurrentUser();
  this.router.navigate(['/auth/login']);
});
```

### Verificar Autenticación

```typescript
if (this.authService.isAuthenticated()) {
  const currentUser = this.authService.getCurrentUser();
  console.log('Usuario actual:', currentUser);
}
```

---

## 📊 Uso de Servicios

### Obtener datos

```typescript
this.productoService.getAll().subscribe({
  next: (productos) => console.log(productos),
  error: (error) => console.error(error)
});
```

### Crear registro

```typescript
this.productoService.create(nuevoProducto).subscribe({
  next: (producto) => console.log('Creado:', producto),
  error: (error) => console.error(error)
});
```

### Actualizar registro

```typescript
this.productoService.update(id, datosActualizados).subscribe({
  next: (producto) => console.log('Actualizado:', producto),
  error: (error) => console.error(error)
});
```

### Eliminar registro

```typescript
this.productoService.delete(id).subscribe({
  next: () => console.log('Eliminado'),
  error: (error) => console.error(error)
});
```

---

## 🎯 Prioridades de Desarrollo

### Alta Prioridad (Semana 1-2)
1. ✅ Completar módulo de autenticación (login funcional)
2. ✅ Implementar dashboard básico para cada rol
3. ✅ Crear CRUD completo de productos
4. ✅ Implementar gestión básica de inventario

### Media Prioridad (Semana 3-4)
1. ⏳ Implementar POS (punto de venta)
2. ⏳ Crear gestión de ventas
3. ⏳ Implementar módulo de caja
4. ⏳ Desarrollar gestión de clientes

### Baja Prioridad (Semana 5+)
1. ⏳ Sistema de reportes completo
2. ⏳ Gestión de proveedores y órdenes
3. ⏳ Parámetros del sistema
4. ⏳ Optimizaciones y mejoras de UI

---

## 🐛 Debugging

### Ver errores en la consola

```typescript
// Agregar logs en servicios
console.log('Datos recibidos:', data);
console.error('Error:', error);
```

### Verificar llamadas HTTP

1. Abrir Chrome DevTools (F12)
2. Ir a la pestaña "Network"
3. Filtrar por "XHR" o "Fetch"
4. Verificar las peticiones y respuestas

### Errores comunes

**Error: Can't resolve '@angular/material'**
```bash
npm install @angular/material@20 @angular/cdk@20 @angular/animations@20
```

**Error: HttpClient not found**
- Verificar que `provideHttpClient()` esté en `app.config.ts`

**Error: Route not found**
- Verificar que las rutas estén configuradas correctamente
- Verificar que los módulos se estén importando

---

## 📚 Recursos Adicionales

- [Angular Documentation](https://angular.dev/)
- [Angular Material](https://material.angular.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [RxJS Documentation](https://rxjs.dev/)

---

## 👥 Contacto y Soporte

Para dudas o problemas, contactar al equipo de desarrollo.

**¡Buena suerte con el desarrollo! 🚀**
