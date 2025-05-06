-- Crear tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,  -- El campo 'usuario' para identificar al usuario
    password VARCHAR(100) NOT NULL,       -- Contraseña (campo 'password' para seguridad)
    
    -- Campos adicionales para completar la autenticación
    is_active BOOLEAN DEFAULT TRUE,       -- Usuario activo (por defecto True)
    is_staff BOOLEAN DEFAULT FALSE,       -- ¿Es personal administrativo? (por defecto False)
    is_superuser BOOLEAN DEFAULT FALSE,   -- ¿Es superusuario? (por defecto False)
    
    -- Campos adicionales
    last_login TIMESTAMP,                 -- Último inicio de sesión
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha en que el usuario se creó (por defecto la fecha actual)
    email VARCHAR(255) UNIQUE,            -- Correo electrónico del usuario (opcional)
    
    -- El resto de los campos ya definidos en el modelo de Django
    CONSTRAINT email_check CHECK (email IS NULL OR email != '')
);
-- Crear tabla de sesiones (django_session)
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,          -- Clave única de la sesión (identificador de la sesión)
    session_data TEXT NOT NULL,                   -- Datos serializados de la sesión
    expire_date TIMESTAMP NOT NULL               -- Fecha de expiración de la sesión
);

-- Crear tabla de datos
CREATE TABLE datos (
    id SERIAL PRIMARY KEY,
    tipo_registro VARCHAR(20) CHECK (tipo_registro IN ('mantenimiento', 'averia', 'consumo')) NOT NULL,
    kilometraje INTEGER NOT NULL,
    precio DECIMAL(10, 2),
    fecha DATE NOT NULL,
    detalles TEXT,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Insertar usuarios de prueba
INSERT INTO usuarios (usuario, password, is_active, is_staff, is_superuser, email) VALUES
('juan', 'clave123', TRUE, FALSE, FALSE, 'juan@correo.com'),
('maria', 'pass456', TRUE, FALSE, FALSE, 'maria@correo.com');

-- Insertar datos para el usuario 'juan' (id = 1)
INSERT INTO datos (tipo_registro, kilometraje, precio, fecha, detalles, usuario_id) VALUES
('mantenimiento', 12000, 250.00, '2024-10-15', 'Cambio de aceite y filtro', 1),
('averia', 13500, 400.00, '2024-12-01', 'Fallo en el sistema de frenos', 1),
('consumo', 14000, 60.00, '2025-01-20', 'Llenado de combustible', 1);

-- Insertar datos para el usuario 'maria' (id = 2)
INSERT INTO datos (tipo_registro, kilometraje, precio, fecha, detalles, usuario_id) VALUES
('mantenimiento', 10000, 180.00, '2024-11-05', 'Revisión general', 2),
('averia', 11000, 320.00, '2025-02-10', 'Problema en la caja de cambios', 2),
('consumo', 11500, 55.00, '2025-03-01', 'Repostaje en autopista', 2);
