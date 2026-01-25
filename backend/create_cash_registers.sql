-- Script para crear cajas registradoras iniciales
-- Ejecutar este script en la base de datos para crear cajas si no existen

-- Insertar cajas registradoras solo si no existen
INSERT INTO cash_registers (id, register_number, location, is_active)
SELECT 
    gen_random_uuid(),
    'Caja Principal',
    'Piso 1 - Entrada',
    true
WHERE NOT EXISTS (
    SELECT 1 FROM cash_registers WHERE register_number = 'Caja Principal'
);

INSERT INTO cash_registers (id, register_number, location, is_active)
SELECT 
    gen_random_uuid(),
    'Caja 2',
    'Piso 1 - Salida',
    true
WHERE NOT EXISTS (
    SELECT 1 FROM cash_registers WHERE register_number = 'Caja 2'
);

INSERT INTO cash_registers (id, register_number, location, is_active)
SELECT 
    gen_random_uuid(),
    'Caja Express',
    'Piso 2',
    true
WHERE NOT EXISTS (
    SELECT 1 FROM cash_registers WHERE register_number = 'Caja Express'
);

-- Verificar las cajas creadas
SELECT id, register_number, location, is_active 
FROM cash_registers 
ORDER BY register_number;
