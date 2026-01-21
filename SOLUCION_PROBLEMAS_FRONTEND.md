# 🔧 SOLUCIÓN DE PROBLEMAS - FRONTEND NO CARGA DATOS

## ✅ PROBLEMAS IDENTIFICADOS Y RESUELTOS

### 1. Base de Datos Sin Datos Iniciales ✅ RESUELTO
**Problema**: La base de datos estaba vacía, por lo que no había usuarios, productos, ni datos para mostrar.

**Solución Aplicada**:
```bash
cd backend
.\.venv\Scripts\python reset_database.py
```

**Resultado**:
- ✅ Tablas creadas
- ✅ Datos iniciales insertados
- ✅ Usuario de prueba disponible

**Credenciales de prueba**:
- Username: `admin`
- Password: `admin123`

---

### 2. Backend Corriendo ✅ VERIFICADO
**Estado**: Backend corriendo en http://localhost:8000

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## 🧪 PRUEBAS DE VERIFICACIÓN

### Prueba 1: Login Funcional
```bash
# Desde PowerShell
$body = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$response
```

**Resultado Esperado**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "username": "admin",
    "email": "admin@minimercado.com",
    "first_name": "Justin",
    "last_name": "Admin",
    "profile_name": "Administrador"
  }
}
```

### Prueba 2: Obtener Usuarios
```bash
# Obtener token primero (ver Prueba 1)
$token = $response.access_token

# Obtener lista de usuarios
$users = Invoke-RestMethod -Uri "http://localhost:8000/users" `
    -Method Get `
    -Headers @{Authorization="Bearer $token"}

$users
```

**Resultado Esperado**: Lista de 5 usuarios con datos completos

### Prueba 3: Obtener Productos
```bash
$products = Invoke-RestMethod -Uri "http://localhost:8000/products" `
    -Method Get `
    -Headers @{Authorization="Bearer $token"}

$products
```

**Resultado Esperado**: Lista de productos con categorías y marcas

---

## 🌐 INICIAR EL FRONTEND ANGULAR

### Paso 1: Instalar dependencias (si es primera vez)
```bash
cd Frontend
npm install
```

### Paso 2: Iniciar servidor de desarrollo
```bash
ng serve --port 4200
```

### Paso 3: Acceder a la aplicación
```
http://localhost:4200
```

### Paso 4: Login
- Usuario: `admin`
- Contraseña: `admin123`

---

## 🔍 CHECKLIST DE DIAGNÓSTICO

### Backend
- [✅] Backend corriendo en http://localhost:8000
- [✅] Base de datos inicializada con datos
- [✅] Endpoint /docs accesible
- [✅] Login funciona (POST /auth/login)
- [✅] CORS configurado para localhost:4200

### Frontend
- [ ] npm install ejecutado
- [ ] ng serve corriendo en puerto 4200
- [ ] environment.apiUrl apunta a http://localhost:8000
- [ ] Interceptor de auth configurado
- [ ] localStorage limpio (si hay problemas)

---

## 🚨 SI EL FRONTEND SIGUE SIN CARGAR DATOS

### Paso 1: Limpiar localStorage del navegador
```javascript
// En la consola del navegador (F12)
localStorage.clear()
location.reload()
```

### Paso 2: Verificar consola del navegador
1. Abrir DevTools (F12)
2. Ir a pestaña "Console"
3. Buscar errores en rojo
4. Buscar errores 401, 403, 404, 500

**Errores comunes**:
- `401 Unauthorized` → Token inválido o expirado (hacer logout/login)
- `404 Not Found` → Endpoint no existe (verificar URL en service)
- `CORS error` → Backend no permite peticiones desde frontend

### Paso 3: Verificar pestaña Network
1. Abrir DevTools (F12)
2. Ir a pestaña "Network"
3. Recargar página
4. Ver peticiones HTTP
5. Click en petición que falla
6. Ver "Response" y "Headers"

**Verificar**:
- ✅ Request URL: `http://localhost:8000/...`
- ✅ Request Method: GET, POST, etc.
- ✅ Status Code: 200 (éxito)
- ✅ Response Headers incluyen `access-control-allow-origin`

### Paso 4: Probar endpoints directamente
```bash
# Test de Dashboard
curl http://localhost:8000/dashboard/metrics -H "Authorization: Bearer <token>"

# Test de Usuarios
curl http://localhost:8000/users -H "Authorization: Bearer <token>"

# Test de Productos
curl http://localhost:8000/products -H "Authorization: Bearer <token>"
```

---

## 📊 DATOS DE PRUEBA DISPONIBLES

### Usuarios (5)
- `admin` / `admin123` (Administrador)
- `ana_caja` / `admin123` (Cajero)
- `carlos_inv` / `admin123` (Inventario)
- `maria_ger` / `admin123` (Gerente)
- `luis_sup` / `admin123` (Supervisor)

### Productos (10)
- Coca Cola 500ml
- Leche Entera
- Arroz Blanco
- Papel Higiénico
- Jabón Líquido
- Pan Blanco
- Pollo Fresco
- Café Molido
- Detergente
- Galletas Chocolate

### Categorías (10)
- Abarrotes
- Bebidas
- Limpieza
- Lácteos
- Carnes
- Snacks
- Panadería
- Higiene Personal
- Mascotas
- Frutas y Verduras

### Proveedores (5)
- Distribuidora Nacional
- Lácteos del Valle
- Carnes Premium
- Limpieza Total
- Panadería Artesanal

---

## 🔧 SCRIPTS ÚTILES

### Reiniciar Base de Datos
```bash
cd backend
.\.venv\Scripts\python reset_database.py
```

### Verificar Backend
```bash
cd backend
.\.venv\Scripts\python -c "from app.main import app; print('✅ Backend OK')"
```

### Verificar Conexión DB
```bash
cd backend
.\.venv\Scripts\python -c "from app.db.database import engine; from sqlmodel import select, Session; from app.models.models import User; session = Session(engine); users = session.exec(select(User)).all(); print(f'✅ {len(users)} usuarios en DB')"
```

---

## 🎯 PASOS FINALES

1. ✅ Backend corriendo: http://localhost:8000
2. ✅ Base de datos con datos
3. [ ] Frontend corriendo: http://localhost:4200
4. [ ] Login exitoso con admin/admin123
5. [ ] Dashboard carga datos
6. [ ] Usuarios lista carga
7. [ ] Productos lista carga

---

## 📞 SI PERSISTEN PROBLEMAS

### Logs del Backend
Revisa el terminal donde corre uvicorn. Busca:
- `ERROR` en rojo
- `WARNING` en amarillo
- Stack traces de Python

### Logs del Frontend
Revisa la consola del navegador (F12). Busca:
- Errores HTTP (401, 404, 500)
- CORS errors
- JavaScript errors

### Reportar problema
Incluye:
1. Mensaje de error exacto
2. Endpoint que falla
3. Screenshot de consola
4. Screenshot de Network tab

---

**Última actualización**: 2025-01-20  
**Backend**: ✅ FUNCIONANDO  
**Base de datos**: ✅ POBLADA  
**Estado**: LISTO PARA PRUEBAS
