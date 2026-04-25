
# Pruebas del Sistema — FerreteriaStock

Este documento describe las estrategias de pruebas aplicadas al sistema de gestión de inventario desarrollado con Flask y Supabase.

---

## 1. Pruebas Unitarias

### Módulo seleccionado

Se selecciona la siguiente lógica de negocio:

**Validación de salida de stock**

Regla:
> No se puede retirar más stock del disponible.

---

### Parámetros de entrada

- `stock_actual`: cantidad disponible del producto  
- `cantidad_salida`: cantidad que se desea retirar  

---

### Clases de equivalencia

| Tipo        | Descripción                  | Ejemplo    | Resultado esperado |
|------------|------------------------------|-----------|--------------------|
| Válida      | Salida menor al stock        | (10, 5)   | Permitido          |
| Válida límite | Salida igual al stock      | (10, 10)  | Permitido          |
| Inválida    | Salida mayor al stock        | (10, 11)  | Rechazado          |
| Inválida    | Cantidad menor o igual a 0   | (10, 0)   | Rechazado          |
| Inválida    | Stock negativo               | (-5, 2)   | Rechazado          |

---

### Valores límite

Para `stock_actual = 10`:

| Caso              | Entrada | Resultado esperado |
|------------------|--------|------------------|
| Antes del límite | 9      | Permitido        |
| En el límite     | 10     | Permitido        |
| Después del límite | 11   | Rechazado        |

---

### Casos de prueba

- **Caso 1 — válido**
  - Entrada: stock_actual=10, cantidad=5  
  - Resultado esperado: operación permitida  

- **Caso 2 — límite**
  - Entrada: stock_actual=10, cantidad=10  
  - Resultado esperado: operación permitida  

- **Caso 3 — inválido**
  - Entrada: stock_actual=10, cantidad=11  
  - Resultado esperado: operación rechazada  

---

### Framework recomendado

Se recomienda utilizar **pytest**.

**Justificación:**
- Es el estándar en Python
- Compatible con Flask
- Sintaxis simple y clara (`assert`)
- Permite testear lógica sin depender de la base de datos

---

### Ejemplo de test

```python
def validar_salida_stock(stock_actual, cantidad):
    if stock_actual < 0:
        return False
    if cantidad <= 0:
        return False
    if cantidad > stock_actual:
        return False
    return True


def test_validacion_salida_stock():
    assert validar_salida_stock(10, 5) == True
    assert validar_salida_stock(10, 10) == True
    assert validar_salida_stock(10, 11) == False
````

---

## 2. Pruebas de Integración

### Dependencias externas

El sistema interactúa con:

1. **Base de datos (Supabase)**

   * Productos
   * Movimientos de stock
   * Alertas

2. **Sistema de autenticación (Supabase Auth)**

   * Login de usuarios
   * Control de roles

---

### Uso de mocks / stubs

Para evitar depender de servicios reales, se utilizan **mocks** que simulan:

* respuestas de la base de datos
* comportamiento de servicios externos

Esto permite probar la lógica de forma aislada.

---

### Ejemplo de prueba de integración

Caso:

> Registrar un movimiento de entrada de stock

**Flujo:**

1. Simular un producto existente
2. Ejecutar la función de registro
3. Verificar actualización de stock
4. Verificar registro del movimiento

---

### Pseudocódigo

```python
def test_registro_movimiento(mock_db):
    mock_db.get_producto.return_value = {"stock_actual": 10}

    nuevo_stock = registrar_movimiento(
        producto_id=1,
        tipo="entrada",
        cantidad=5
    )

    assert nuevo_stock == 15
    mock_db.update_producto.assert_called()
    mock_db.insert_movimiento.assert_called()
```

---

### Herramientas recomendadas

* `unittest.mock`
* `pytest-mock`

**Justificación:**

* Permiten simular dependencias externas
* Integración directa con Python
* Uso estándar en proyectos Flask

---

## 3. Pruebas de Componentes y de Sistema

### Componente seleccionado

**Módulo de gestión de stock**

Incluye:

* registro de productos
* movimientos de stock
* generación de alertas
* importación de Excel

---

### Prueba de componente

Se prueba el módulo de forma aislada.

**Entradas:**

* producto con stock inicial
* movimiento (entrada o salida)

**Salidas esperadas:**

* stock actualizado correctamente
* alerta generada si corresponde

---

### Pruebas de sistema

Caso crítico:

> Carga de stock desde archivo Excel de proveedor

---

### Flujo completo

1. Usuario inicia sesión
2. Accede a importar Excel
3. Sube archivo
4. Sistema procesa datos
5. Se actualiza el stock
6. Se registran movimientos
7. Se generan alertas

---

### Validaciones

| Paso          | Validación             |
| ------------- | ---------------------- |
| Login         | Usuario autenticado    |
| Archivo       | Formato válido (.xlsx) |
| Procesamiento | Lectura correcta       |
| Stock         | Actualización correcta |
| Movimiento    | Registro guardado      |
| Alertas       | Generación correcta    |

---

### Herramientas End-to-End

**Cypress**

* Fácil de usar
* Rápido

**Playwright**

* Soporta múltiples navegadores
* Más robusto

**Selenium**

* Más complejo
* Menos eficiente

---

### Herramienta elegida: Playwright

**Justificación:**

* Permite probar flujos completos
* Mayor compatibilidad
* Ideal para sistemas con múltiples vistas y lógica compleja

---

## Conclusión

Las pruebas implementadas permiten:

* Validar reglas críticas del sistema
* Detectar errores antes de producción
* Asegurar estabilidad tras la migración a Supabase

Se combinan:

* pruebas unitarias → lógica interna
* pruebas de integración → interacción con servicios
* pruebas de sistema → flujo completo del usuario

Esto garantiza una cobertura adecuada del sistema.

````
