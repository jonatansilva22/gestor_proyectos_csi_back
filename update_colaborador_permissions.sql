-- Script SQL para actualizar permisos del colaborador
-- Ejecutar directamente en la base de datos

-- 1. Insertar permisos si no existen
INSERT INTO permissions (name) 
VALUES ('view_user') 
ON CONFLICT (name) DO NOTHING;

INSERT INTO permissions (name) 
VALUES ('change_user') 
ON CONFLICT (name) DO NOTHING;

-- 2. Asignar permisos al rol colaborador (ID = 3)
-- Verificar que el rol colaborador existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM role_types WHERE id = 3) THEN
        RAISE EXCEPTION 'Rol colaborador (ID: 3) no encontrado. Verifica que existe en role_types.';
    END IF;
END $$;

-- Asignar view_user al colaborador
INSERT INTO role_permissions (role_id, permission_id) 
SELECT 3, p.id 
FROM permissions p 
WHERE p.name = 'view_user'
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- Asignar change_user al colaborador  
INSERT INTO role_permissions (role_id, permission_id)
SELECT 3, p.id 
FROM permissions p 
WHERE p.name = 'change_user'
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- 3. Verificar resultados
SELECT 
    'Permisos actualizados correctamente para el rol colaborador' AS mensaje;

-- Mostrar todos los permisos del colaborador
SELECT 
    rt.id as role_id,
    rt.name as role_name,
    p.name as permission_name
FROM role_permissions rp
JOIN role_types rt ON rp.role_id = rt.id  
JOIN permissions p ON rp.permission_id = p.id
WHERE rt.id = 3
ORDER BY p.name;

-- Mostrar resumen de todos los roles y permisos
SELECT 
    rt.id as role_id,
    rt.name as role_name, 
    COUNT(rp.permission_id) as total_permissions
FROM role_types rt
LEFT JOIN role_permissions rp ON rt.id = rp.role_id
GROUP BY rt.id, rt.name
ORDER BY rt.id;