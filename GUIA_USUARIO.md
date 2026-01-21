# 🚀 GUÍA RÁPIDA - CÓMO USAR EL SISTEMA

## ✅ ¿QUÉ SE HA SOLUCIONADO?

### Problema Original
> "Nada funciona - usuarios no cargan, no puedo hacer login con diferentes usuarios, transacciones no funcionan, dashboard vacío, botones rotos, lento e inconsistente, endpoints existen pero no consume ni funciona nada"

### Solución Aplicada
1. ✅ **Base de datos inicializada** con 5 usuarios, 10 productos, 10 categorías, 5 proveedores
2. ✅ **Backend corriendo** en http://localhost:8000 con 87 endpoints
3. 🟡 **Frontend iniciado** en http://localhost:4200 (con errores de compilación)

---

## 🎯 ESTADO ACTUAL

| Componente | Estado | Detalles |
|------------|--------|----------|
| **PostgreSQL** | ✅ FUNCIONANDO | Base de datos poblada |
| **Backend (FastAPI)** | ✅ FUNCIONANDO | Puerto 8000, auto-reload activo |
| **Frontend (Angular)** | ⚠️ EN DESARROLLO | Puerto 4200, compilando con errores |

---

## 🔑 CREDENCIALES DE ACCESO

### Usuario Administrador
```
Usuario: admin
Password: admin123
```

### Otros Usuarios de Prueba
```
Cajero:     ana_caja / admin123
Inventario: carlos_inv / admin123
Gerente:    maria_ger / admin123
Supervisor: luis_sup / admin123
```

---

## 🌐 ACCEDER A LA APLICACIÓN

### 1. Verificar que Backend está corriendo
Abrir navegador en: **http://localhost:8000/docs**

✅ Si ves la documentación Swagger = Backend OK

### 2. Acceder al Frontend
Abrir navegador en: **http://localhost:4200**

⚠️ Puede tardar en cargar por los errores de compilación

### 3. Hacer Login
1. Ir a la página de login
2. Ingresar: `admin` / `admin123`
3. Click en "Iniciar Sesión"

**Qué esperar**:
- ✅ Token guardado en localStorage
- ✅ Redirección al dashboard
- ✅ Menú de navegación visible

---

## 🧪 PROBAR FUNCIONALIDAD

### Test 1: Dashboard
1. Ir a http://localhost:4200
2. Login con admin/admin123
3. Dashboard debería mostrar:
   - Total de ventas
   - Productos disponibles
   - Usuarios activos
   - Estado de caja

**Si no carga datos**: Ver sección "Diagnóstico" abajo

### Test 2: Usuarios
1. Ir a módulo "Usuarios" (menú lateral o /users)
2. Debería cargar lista de 5 usuarios
3. Probar crear nuevo usuario
4. Probar editar usuario existente

### Test 3: Productos
1. Ir a módulo "Productos"
2. Debería cargar 10 productos con:
   - Nombre, categoría, marca
   - Precio compra/venta
   - Stock actual
3. Probar crear nuevo producto
4. Probar editar producto

### Test 4: Ventas
1. Ir a módulo "Ventas" o "POS"
2. Seleccionar productos
3. Agregar al carrito
4. Procesar venta
5. Verificar que se guarda

---

## 🔍 DIAGNÓSTICO DE PROBLEMAS

### Problema: "Login no funciona"

**Solución 1: Limpiar localStorage**
```javascript
// En consola del navegador (F12)
localStorage.clear()
location.reload()
```

**Solución 2: Verificar backend**
```powershell
curl http://localhost:8000/docs
# Debería responder con HTML
```

**Solución 3: Probar login directo**
```powershell
$body = @{username="admin"; password="admin123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method Post -Body $body -ContentType "application/json"
```

---

### Problema: "Dashboard vacío / No carga datos"

**Verificar en DevTools (F12)**:

1. **Consola (Console)**
   - Buscar errores en rojo
   - Buscar `401 Unauthorized` → Token expirado, hacer logout/login
   - Buscar `CORS error` → Backend no responde

2. **Red (Network)**
   - Ver peticiones HTTP
   - Verificar que vayan a `http://localhost:8000/...`
   - Ver Response de cada petición
   - Status 200 = OK, 401 = No autenticado, 404 = Endpoint no existe

**Verificar token**:
```javascript
// En consola del navegador (F12)
const user = JSON.parse(localStorage.getItem('user') || '{}');
console.log('Token:', user.token);
console.log('Role:', user.role);
```

---

### Problema: "Botones no responden / Vistas no cargan"

**Causas posibles**:
1. Errores JavaScript bloqueando ejecución
2. Token inválido
3. CORS bloqueado
4. Endpoint incorrecto

**Solución**:
1. Abrir DevTools (F12)
2. Ver consola
3. Recargar página (Ctrl+R)
4. Identificar error específico
5. Reportar error con screenshot

---

### Problema: "No puedo crear/editar/eliminar"

**Verificar permisos**:
```javascript
// En consola del navegador (F12)
const user = JSON.parse(localStorage.getItem('user') || '{}');
console.log('Usuario actual:', user.username);
console.log('Rol:', user.role);
```

El usuario `admin` tiene todos los permisos. Si usas otro usuario, verifica su rol.

---

## 📊 DATOS DISPONIBLES PARA PROBAR

### Productos Existentes
- Coca Cola 500ml (Bebidas) - $1.20
- Leche Entera (Lácteos) - $1.50
- Arroz Blanco (Abarrotes) - $2.00
- Papel Higiénico (Higiene) - $5.00
- Pan Blanco (Panadería) - $1.00

### Categorías
Abarrotes, Bebidas, Limpieza, Lácteos, Carnes, Snacks, Panadería, Higiene Personal, Mascotas, Frutas y Verduras

### Proveedores
Distribuidora Nacional, Lácteos del Valle, Carnes Premium, Limpieza Total, Panadería Artesanal

---

## 🛠️ SCRIPTS DE AYUDA

### Reiniciar Backend y Frontend
```cmd
INICIAR_SISTEMA.bat
```

### Probar Todos los Endpoints
```powershell
powershell -ExecutionPolicy Bypass -File test_endpoints.ps1
```

### Reiniciar Base de Datos
```powershell
cd backend
.\.venv\Scripts\python reset_database.py
```

---

## 🚨 SI NADA FUNCIONA

### Reinicio Completo

1. **Detener servicios**
   - Cerrar terminal del backend (Ctrl+C)
   - Cerrar terminal del frontend (Ctrl+C)

2. **Reiniciar base de datos**
   ```powershell
   cd backend
   .\.venv\Scripts\python reset_database.py
   ```

3. **Reiniciar backend**
   ```powershell
   cd backend
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
   ```

4. **Reiniciar frontend**
   ```powershell
   cd Frontend
   npx -y @angular/cli serve --port 4200
   ```

5. **Limpiar navegador**
   - Abrir DevTools (F12)
   - Application → Storage → Clear site data
   - Recargar página

---

## 📞 REPORTAR PROBLEMAS

Si encuentras un problema, proporciona:

1. **Descripción del problema**
   - Qué estabas intentando hacer
   - Qué esperabas que pasara
   - Qué pasó en realidad

2. **Información técnica**
   - Screenshot de la consola del navegador (F12)
   - Screenshot de la pestaña Network (F12)
   - Logs del terminal del backend
   - URL donde ocurrió el error

3. **Pasos para reproducir**
   - Paso 1: ...
   - Paso 2: ...
   - Paso 3: ...

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de reportar un problema, verifica:

- [ ] Backend corriendo en http://localhost:8000
- [ ] Frontend corriendo en http://localhost:4200
- [ ] Base de datos tiene datos (verificar con reset_database.py)
- [ ] localStorage limpio
- [ ] Consola del navegador sin errores críticos
- [ ] Token válido (hacer logout/login)
- [ ] CORS permitido (verificar en Network)

---

**Última actualización**: 2025-01-20  
**Versión Backend**: FastAPI + PostgreSQL  
**Versión Frontend**: Angular  
**Estado**: Backend funcional | Frontend en desarrollo
