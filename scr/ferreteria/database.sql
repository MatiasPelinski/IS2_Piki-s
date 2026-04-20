-- ============================================================
-- BASE DE DATOS PARA SISTEMA DE INVENTARIO FERRETERÍA
-- Proyecto: Stockeado
-- ============================================================

CREATE DATABASE IF NOT EXISTS ferreteria_stock
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ferreteria_stock;

-- ============================================================
-- TABLA: categorias
-- ============================================================
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA: proveedores
-- ============================================================
CREATE TABLE proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    contacto VARCHAR(150),
    telefono VARCHAR(30),
    email VARCHAR(150),
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA: usuarios
-- ============================================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('empleado', 'encargado') NOT NULL DEFAULT 'empleado',
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA: productos
-- ============================================================
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(255),
    precio DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 0,
    id_categoria INT,
    id_proveedor INT,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_producto_categoria
        FOREIGN KEY (id_categoria) REFERENCES categorias(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor) REFERENCES proveedores(id)
        ON DELETE SET NULL
);

-- ============================================================
-- TABLA: movimientos_stock
-- ============================================================
CREATE TABLE movimientos_stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('entrada', 'salida', 'ajuste') NOT NULL,
    cantidad INT NOT NULL,
    motivo VARCHAR(255),
    id_producto INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_movimiento_producto
        FOREIGN KEY (id_producto) REFERENCES productos(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_movimiento_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        ON DELETE RESTRICT
);

-- ============================================================
-- TABLA: alertas
-- ============================================================
CREATE TABLE alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL DEFAULT 'stock_bajo',
    mensaje VARCHAR(255),
    id_producto INT NOT NULL,
    resuelta TINYINT(1) NOT NULL DEFAULT 0,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_alerta_producto
        FOREIGN KEY (id_producto) REFERENCES productos(id)
        ON DELETE CASCADE
);

-- ============================================================
-- TABLA: ordenes_reposicion
-- ============================================================
CREATE TABLE ordenes_reposicion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estado ENUM('pendiente', 'enviada', 'recibida', 'cancelada') NOT NULL DEFAULT 'pendiente',
    id_proveedor INT,
    id_usuario INT NOT NULL,
    observaciones VARCHAR(255),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orden_proveedor
        FOREIGN KEY (id_proveedor) REFERENCES proveedores(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_orden_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        ON DELETE RESTRICT
);

-- ============================================================
-- TABLA: ordenes_reposicion_detalle
-- ============================================================
CREATE TABLE ordenes_reposicion_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_orden INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad_solicitada INT NOT NULL,
    CONSTRAINT fk_detalle_orden
        FOREIGN KEY (id_orden) REFERENCES ordenes_reposicion(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_detalle_producto
        FOREIGN KEY (id_producto) REFERENCES productos(id)
        ON DELETE RESTRICT
);

-- ============================================================
-- DATOS DE PRUEBA
-- ============================================================

INSERT INTO categorias (nombre, descripcion) VALUES
('Herramientas manuales', 'Martillos, destornilladores, llaves, etc.'),
('Tornillería', 'Tornillos, tuercas, bulones y arandelas'),
('Pintura', 'Pinturas, esmaltes, diluyentes y accesorios'),
('Electricidad', 'Cables, llaves de luz, tomacorrientes'),
('Plomería', 'Caños, llaves de paso, accesorios');

INSERT INTO proveedores (nombre, contacto, telefono, email) VALUES
('Distribuidora del Norte', 'Carlos Pérez', '3764-000111', 'carlos@distribuidora.com'),
('Ferretera Central SA', 'Laura Gómez', '3764-000222', 'laura@ferreteracentral.com');

INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Encargado', 'admin@ferreteria.com', 'admin123', 'encargado'),
('Juan Empleado', 'juan@ferreteria.com', 'emp123', 'empleado');

INSERT INTO productos (nombre, descripcion, precio, stock_actual, stock_minimo, id_categoria, id_proveedor) VALUES
('Martillo 500g', 'Martillo de carpintero mango madera', 2500.00, 15, 5, 1, 1),
('Tornillo 4x40', 'Tornillo autorroscante cabeza plana', 25.00, 200, 50, 2, 2),
('Pintura látex blanca 4L', 'Pintura látex interior/exterior', 8500.00, 8, 3, 3, 1),
('Cable unipolar 2.5mm', 'Cable eléctrico por metro', 350.00, 100, 20, 4, 2),
('Llave de paso 1/2"', 'Llave de paso esfera PVC', 1200.00, 4, 5, 5, 1);