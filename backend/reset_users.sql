DELETE FROM "user";
DELETE FROM profile;

INSERT INTO profile (id, name, description) VALUES 
  ('550e8400-e29b-41d4-a716-446655440001', 'Administrador', 'Acceso total'),
  ('550e8400-e29b-41d4-a716-446655440002', 'Cajero', 'Solo ventas y caja'),
  ('550e8400-e29b-41d4-a716-446655440003', 'Inventario', 'Gestión de stock');

INSERT INTO "user" (id, username, email, hashed_password, profile_id, first_name, last_name, is_active) VALUES 
  ('550e8400-e29b-41d4-a716-446655440004', 'admin', 'admin@minimercado.com', '$2b$12$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK', '550e8400-e29b-41d4-a716-446655440001', 'Justin', 'Admin', true),
  ('550e8400-e29b-41d4-a716-446655440005', 'ana_caja', 'ana@mail.com', '$2b$12$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK', '550e8400-e29b-41d4-a716-446655440002', 'Ana', 'López', true),
  ('550e8400-e29b-41d4-a716-446655440006', 'carlos_ventas', 'carlos@mail.com', '$2b$12$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK', '550e8400-e29b-41d4-a716-446655440002', 'Carlos', 'Ruiz', true),
  ('550e8400-e29b-41d4-a716-446655440007', 'marta_inv', 'marta@mail.com', '$2b$12$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK', '550e8400-e29b-41d4-a716-446655440003', 'Marta', 'Sosa', true);
