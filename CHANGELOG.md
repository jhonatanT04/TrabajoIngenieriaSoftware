# Sistema de Inventario y Ventas - Registro de Cambios

**Proyecto:** Sistema de Gestión de Inventario y Ventas  
**Stack:** FastAPI (Backend) + Angular (Frontend) + PostgreSQL  
**Última actualización:** 21 de enero de 2026

---

## Configuración del Sistema

### Backend
- Puerto: 8000
- Framework: FastAPI
- Base de datos: PostgreSQL
- Entorno virtual: .venv

### Frontend
- Puerto: 4200
- Framework: Angular
- Servidor de desarrollo: ng serve

---

## Cambios Implementados

### 1. Sistema de Inventario

#### Correcciones de Stock
- Corregido el problema donde el stock siempre mostraba 0
- Implementado cálculo correcto de stock actual basado en movimientos de inventario
- Añadido filtro por producto en historial de movimientos
- Creado script `adjust_min_max.py` para ajustar valores mínimos y máximos de stock

#### Endpoints Modificados
- `GET /inventory/` - Retorna stock actual calculado correctamente
- `GET /inventory/movements` - Añadido parámetro opcional `product_id` para filtrar
- Todos los movimientos de inventario ahora incluyen `previous_stock` y `new_stock`

### 2. Sistema de Ventas

#### Nueva Venta - Funcionalidad Completa
- Implementado formulario completamente funcional para crear ventas
- Carga dinámica de usuarios, clientes y productos desde el backend
- Validación de stock en tiempo real antes de agregar productos
- Productos sin stock se deshabilitan automáticamente en el selector
- Deducción automática de inventario al crear una venta

#### Visualización de Información
- Corregido el display de nombres de clientes (first_name + last_name)
- Añadida información completa del vendedor (cashier) en respuestas del backend
- Implementado mapeo correcto de nombres en venta-list component
- Script `update_users_names.py` para poblar nombres de usuarios en la base de datos

#### Detalle de Venta
- Creado componente venta-detail para mostrar información completa de cada venta
- Display de productos vendidos, cantidades, precios y totales
- Información del cliente y vendedor
- Navegación desde la lista de ventas

#### Eliminación de Ventas
- Implementado sistema de confirmación con modal dialog personalizado
- El inventario NO se restaura al eliminar una venta (comportamiento confirmado como correcto)
- Eliminación solo de registros de venta sin afectar stock actual

#### Validaciones
- Validación de stock disponible antes de permitir agregar productos a una venta
- Mensaje de error si se intenta vender más unidades de las disponibles
- Prevención de overselling mediante validación en backend

### 3. Componentes de UI

#### Dialog Component
- Creado componente reutilizable de diálogo modal
- Reemplaza confirmaciones de navegador (window.confirm)
- Estilo consistente con el diseño del sistema
- Soporte para confirmaciones y cancelaciones

#### Mejoras en Formularios
- Display de stock disponible en selector de productos
- Formato: "Nombre - Precio (Stock: X)"
- Deshabilitación automática de productos sin stock

### 4. Correcciones de Backend

#### CORS
- Configuración correcta de CORS para permitir comunicación frontend-backend
- Permitidos los orígenes necesarios para desarrollo

#### Modelos
- Añadidos campos `previous_stock` y `new_stock` a InventoryMovement
- Estructura correcta de respuesta para ventas con información de cashier y customer

#### Validaciones
- Validación de stock antes de crear ventas
- HTTPException 400 si stock insuficiente
- Transacciones atómicas para garantizar consistencia de datos

### 5. Scripts de Utilidad

#### adjust_min_max.py
- Ajusta automáticamente min_stock y max_stock de productos
- Valores basados en stock actual para evitar alertas innecesarias

#### update_users_names.py
- Actualiza campos first_name y last_name de usuarios
- Genera nombres basados en username si están vacíos
- Garantiza que todos los usuarios tengan nombres para display

### 6. Arquitectura y Servicios

#### Frontend Services
- VentaService: Gestión completa de ventas (create, read, delete, list)
- InventarioService: Consulta de stock y movimientos
- ProductoService: Gestión de productos
- UsuarioService: Gestión de usuarios
- ClienteService: Gestión de clientes

#### Backend Routers
- router_venta.py: Endpoints de ventas con validaciones
- router_inventario.py: Gestión de inventario y movimientos
- router_productos.py: CRUD de productos
- router_user.py: Gestión de usuarios
- router_cliente.py: Gestión de clientes

---

## Comportamiento del Sistema

### Flujo de Creación de Venta
1. Usuario selecciona cajero/vendedor
2. Usuario selecciona cliente (o Cliente General por defecto)
3. Usuario añade productos validando stock disponible
4. Sistema muestra stock actual de cada producto
5. Usuario no puede añadir productos sin stock
6. Al guardar, se crea la venta y se deduce automáticamente el inventario

### Flujo de Eliminación de Venta
1. Usuario hace clic en eliminar desde la lista
2. Aparece modal de confirmación personalizado
3. Usuario confirma eliminación
4. Sistema elimina registro de venta SIN restaurar inventario
5. Lista se actualiza automáticamente

### Gestión de Stock
- Stock calculado en base a movimientos de inventario
- Cada venta genera un movimiento de tipo SALE con cantidad negativa
- Sistema previene overselling mediante validación en tiempo de creación
- No se permite crear ventas si no hay stock suficiente

---

## Estructura de Datos

### Sale (Venta)
```
{
  id: UUID
  sale_number: string
  sale_date: datetime
  total_amount: decimal
  cashier_id: UUID
  customer_id: UUID
  cashier: {
    id: UUID
    username: string
    first_name: string
    last_name: string
  }
  customer: {
    id: UUID
    first_name: string
    last_name: string
    ...
  }
  items: [SaleItem]
}
```

### InventoryMovement
```
{
  id: UUID
  product_id: UUID
  movement_type: enum
  quantity: int
  previous_stock: int
  new_stock: int
  reason: string
  created_at: datetime
}
```

---

## Próximas Mejoras Planificadas

Esta sección se actualizará según se planifiquen nuevas funcionalidades.

---

## Notas Técnicas

- Auto-reload activado en backend (uvicorn)
- Watch mode activo en frontend (ng serve)
- Base de datos PostgreSQL con migraciones manuales
- Autenticación temporalmente deshabilitada para desarrollo
- Todos los endpoints requieren configuración de CORS apropiada

---

## Comandos Útiles

### Iniciar Backend
```bash
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### Iniciar Frontend
```bash
cd Frontend
ng serve
```

### Actualizar Base de Datos
```bash
cd backend
.\.venv\Scripts\python.exe update_users_names.py
.\.venv\Scripts\python.exe adjust_min_max.py
```
