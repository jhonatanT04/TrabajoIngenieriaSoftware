# Script PowerShell para probar todos los endpoints
$baseUrl = "http://localhost:8000"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PRUEBA DE ENDPOINTS - MINIMERCADO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Login
Write-Host "[TEST 1] Login..." -ForegroundColor Yellow
try {
    $loginBody = @{
        username = "admin"
        password = "admin123"
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" `
        -Method Post `
        -Body $loginBody `
        -ContentType "application/json"
    
    $token = $loginResponse.access_token
    Write-Host "✅ Login exitoso" -ForegroundColor Green
    Write-Host "   Usuario: $($loginResponse.user.username)" -ForegroundColor Gray
    Write-Host "   Rol: $($loginResponse.user.profile_name)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Error en login: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Headers con token
$headers = @{
    Authorization = "Bearer $token"
}

# Test 2: Dashboard
Write-Host "[TEST 2] Dashboard..." -ForegroundColor Yellow
try {
    $dashboard = Invoke-RestMethod -Uri "$baseUrl/dashboard/metrics" -Headers $headers
    Write-Host "✅ Dashboard OK" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en dashboard: $_" -ForegroundColor Red
}

# Test 3: Usuarios
Write-Host "[TEST 3] Usuarios..." -ForegroundColor Yellow
try {
    $users = Invoke-RestMethod -Uri "$baseUrl/users" -Headers $headers
    Write-Host "✅ Usuarios OK - $($users.Count) usuarios encontrados" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en usuarios: $_" -ForegroundColor Red
}

# Test 4: Productos
Write-Host "[TEST 4] Productos..." -ForegroundColor Yellow
try {
    $products = Invoke-RestMethod -Uri "$baseUrl/products" -Headers $headers
    Write-Host "✅ Productos OK - $($products.Count) productos encontrados" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en productos: $_" -ForegroundColor Red
}

# Test 5: Categorías
Write-Host "[TEST 5] Categorías..." -ForegroundColor Yellow
try {
    $categories = Invoke-RestMethod -Uri "$baseUrl/categories" -Headers $headers
    Write-Host "✅ Categorías OK - $($categories.Count) categorías encontradas" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en categorías: $_" -ForegroundColor Red
}

# Test 6: Proveedores
Write-Host "[TEST 6] Proveedores..." -ForegroundColor Yellow
try {
    $suppliers = Invoke-RestMethod -Uri "$baseUrl/suppliers" -Headers $headers
    Write-Host "✅ Proveedores OK - $($suppliers.Count) proveedores encontrados" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en proveedores: $_" -ForegroundColor Red
}

# Test 7: Clientes
Write-Host "[TEST 7] Clientes..." -ForegroundColor Yellow
try {
    $customers = Invoke-RestMethod -Uri "$baseUrl/customers" -Headers $headers
    Write-Host "✅ Clientes OK - $($customers.Count) clientes encontrados" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en clientes: $_" -ForegroundColor Red
}

# Test 8: Inventario
Write-Host "[TEST 8] Inventario..." -ForegroundColor Yellow
try {
    $inventory = Invoke-RestMethod -Uri "$baseUrl/inventory" -Headers $headers
    Write-Host "✅ Inventario OK - $($inventory.Count) items encontrados" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en inventario: $_" -ForegroundColor Red
}

# Test 9: Ventas
Write-Host "[TEST 9] Ventas..." -ForegroundColor Yellow
try {
    $sales = Invoke-RestMethod -Uri "$baseUrl/sales" -Headers $headers
    Write-Host "✅ Ventas OK - $($sales.Count) ventas encontradas" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en ventas: $_" -ForegroundColor Red
}

# Test 10: Caja
Write-Host "[TEST 10] Sesiones de Caja..." -ForegroundColor Yellow
try {
    $cashSessions = Invoke-RestMethod -Uri "$baseUrl/cash-sessions" -Headers $headers
    Write-Host "✅ Caja OK - $($cashSessions.Count) sesiones encontradas" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en caja: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PRUEBAS COMPLETADAS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Resumen:" -ForegroundColor White
Write-Host "   Backend: http://localhost:8000" -ForegroundColor Gray
Write-Host "   Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "🔑 Credenciales de prueba:" -ForegroundColor White
Write-Host "   Usuario: admin" -ForegroundColor Gray
Write-Host "   Password: admin123" -ForegroundColor Gray
