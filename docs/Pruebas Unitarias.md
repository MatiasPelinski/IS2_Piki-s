# Estrategia de Pruebas — FerreteriaStock

## Contexto del proyecto

FerreteriaStock es un sistema web de gestión de stock para una ferretería. El sistema permite registrar productos, consultar el inventario, registrar movimientos de entrada y salida, generar alertas por stock bajo e importar archivos Excel enviados por proveedores para actualizar cantidades de stock.

El proyecto fue desarrollado inicialmente utilizando **Python Flask**, **HTML/CSS** y una base de datos local con **XAMPP/MySQL**. Actualmente se está realizando una migración hacia **Supabase**, por lo que las pruebas deben considerar tanto la lógica interna del sistema como la interacción con servicios externos, especialmente la base de datos y el sistema de autenticación.

---

## Tipos de pruebas seleccionadas

| Tipo de prueba | ¿Aplica en este proyecto? | Justificación |
|---------------|---------------------------|---------------|
| Unitarias | Sí | Se aplican para verificar funciones puntuales de la lógica de negocio, como validación de salida de stock, cálculo de nuevo stock, control de cantidades inválidas y validación de datos ingresados por formularios. |
| Integración | Sí | Se aplican para comprobar la comunicación entre el backend Flask y servicios externos como Supabase, especialmente en operaciones de consulta de productos, actualización de stock, registro de movimientos y autenticación de usuarios. |
| Componentes | Sí | Se aplican para probar módulos completos de forma aislada, por ejemplo el módulo de gestión de stock, que incluye productos, movimientos, alertas e importación de archivos Excel. |
| Sistema (E2E) | Sí | Se aplican para validar flujos completos desde la perspectiva del usuario, como iniciar sesión, ingresar al dashboard, registrar un movimiento de stock o importar un Excel de proveedor. |
| Regresión | Sí | Se aplican para verificar que los cambios realizados en el sistema, especialmente durante la migración de XAMPP/MySQL a Supabase, no rompan funcionalidades ya implementadas. Se propone automatizarlas mediante GitHub Actions. |
| Estrés | Planificado | Se planifican para una etapa posterior, cuando el sistema tenga endpoints más estables. Servirán para evaluar el comportamiento ante muchas consultas de stock, movimientos simultáneos o cargas masivas de archivos. |

---

## Herramientas gratuitas elegidas

| Nivel de prueba | Herramienta | ¿Qué automatiza en este proyecto? | Justificación |
|----------------|-------------|----------------------------------|---------------|
| Unitarias | pytest | Funciones de validación, reglas de stock y lógica de negocio aislada | Es gratuito, simple, compatible con Python y adecuado para proyectos Flask. |
| Integración | unittest.mock / pytest-mock | Simulación de Supabase, base de datos y autenticación | Permite aislar el componente bajo prueba sin depender de servicios reales. |
| Componentes | pytest + mocks | Módulo de gestión de stock de forma aislada | Permite validar varias funciones relacionadas sin ejecutar todo el sistema completo. |
| Sistema / E2E | Playwright | Flujos completos como login, navegación, carga de Excel y validación visual | Es gratuito, moderno, soporta múltiples navegadores y permite automatizar interacción real del usuario. |
| Regresión | GitHub Actions | Ejecución automática de pruebas en cada push o pull request | Está integrado con GitHub y permite detectar errores antes de integrar cambios. |
| Estrés | Locust | Simulación futura de usuarios concurrentes y carga sobre endpoints | Está escrito en Python y se adapta bien al stack del proyecto. |

---

# 1. Pruebas Unitarias

## 1.1. Módulo o función seleccionada

Se selecciona como función concreta a probar:

**Validar salida de stock**

Esta función representa una regla crítica del sistema: no se debe permitir registrar una salida de stock si la cantidad solicitada es mayor al stock disponible.

La regla de negocio es:

> El sistema debe rechazar cualquier salida de stock que genere valores negativos en el inventario.

Esta validación es importante porque el stock es el dato central del sistema. Si el sistema permite stock negativo, la información del inventario deja de ser confiable y puede afectar decisiones de compra, ventas y reposición.

---

## 1.2. Parámetros de entrada

La función recibe dos parámetros principales:

| Parámetro | Tipo esperado | Descripción |
|----------|--------------|-------------|
| `stock_actual` | Entero | Cantidad disponible actualmente del producto |
| `cantidad_salida` | Entero | Cantidad que se desea retirar del stock |

---

## 1.3. Clases de equivalencia

Las clases de equivalencia permiten agrupar entradas que deberían producir el mismo comportamiento del sistema.

| Clase | Descripción | Ejemplo | Resultado esperado |
|------|-------------|---------|--------------------|
| Válida | La cantidad de salida es menor al stock disponible | `stock_actual = 10`, `cantidad_salida = 5` | Operación permitida |
| Válida límite | La cantidad de salida es igual al stock disponible | `stock_actual = 10`, `cantidad_salida = 10` | Operación permitida |
| Inválida | La cantidad de salida es mayor al stock disponible | `stock_actual = 10`, `cantidad_salida = 11` | Operación rechazada |
| Inválida | La cantidad de salida es cero | `stock_actual = 10`, `cantidad_salida = 0` | Operación rechazada |
| Inválida | La cantidad de salida es negativa | `stock_actual = 10`, `cantidad_salida = -2` | Operación rechazada |
| Inválida | El stock actual es negativo | `stock_actual = -1`, `cantidad_salida = 1` | Operación rechazada |

---

## 1.4. Valores límite

Para un producto con `stock_actual = 10`, los valores límite más relevantes son:

| Caso | Entrada | Resultado esperado |
|-----|---------|--------------------|
| Justo antes del límite | `cantidad_salida = 9` | Permitido |
| En el límite | `cantidad_salida = 10` | Permitido |
| Justo después del límite | `cantidad_salida = 11` | Rechazado |
| Límite inferior inválido | `cantidad_salida = 0` | Rechazado |
| Valor negativo | `cantidad_salida = -1` | Rechazado |

---

## 1.5. Casos de prueba unitaria

### Caso 1 — Salida válida

**Entrada:**

```text
stock_actual = 10
cantidad_salida = 5
```

**Resultado esperado:**

El sistema debe permitir la operación porque existe stock suficiente.

---

### Caso 2 — Salida en el límite

**Entrada:**

```text
stock_actual = 10
cantidad_salida = 10
```

**Resultado esperado:**

El sistema debe permitir la operación. El stock queda en cero, pero no se vuelve negativo.

---

### Caso 3 — Salida inválida por superar el stock

**Entrada:**

```text
stock_actual = 10
cantidad_salida = 11
```

**Resultado esperado:**

El sistema debe rechazar la operación porque generaría stock negativo.

---

## 1.6. Ejemplo de función testeable

```python
def validar_salida_stock(stock_actual, cantidad_salida):
    if stock_actual < 0:
        return False

    if cantidad_salida <= 0:
        return False

    if cantidad_salida > stock_actual:
        return False

    return True
```

---

## 1.7. Ejemplo de test unitario con pytest

```python
from services.stock_service import validar_salida_stock


def test_permite_salida_menor_al_stock():
    assert validar_salida_stock(10, 5) == True


def test_permite_salida_igual_al_stock():
    assert validar_salida_stock(10, 10) == True


def test_no_permite_salida_mayor_al_stock():
    assert validar_salida_stock(10, 11) == False
```

---

## 1.8. Framework de pruebas unitarias recomendado

Para el proyecto se recomienda utilizar **pytest**.

### Justificación

El sistema utiliza principalmente **Python con Flask**, por lo tanto pytest es una herramienta adecuada porque:

- Es gratuita.
- Es ampliamente utilizada en proyectos Python.
- Tiene una sintaxis simple y clara basada en `assert`.
- Permite probar funciones de negocio sin depender de la interfaz HTML.
- Puede integrarse con Flask para probar rutas y formularios.
- Permite combinarse con mocks para simular dependencias externas como Supabase.

La interfaz del sistema está hecha en HTML/CSS, pero la lógica principal se encuentra en Python. Por ese motivo, las pruebas unitarias deben enfocarse principalmente en las funciones del backend.

---

## 1.9. Ubicación sugerida en el repositorio

```text
scr/ferreteria/tests/unit/test_stock_service.py
```

---

# 2. Pruebas de Integración

## 2.1. Objetivo

Las pruebas de integración verifican que distintos módulos del sistema funcionen correctamente en conjunto.

En este proyecto, son especialmente importantes porque el sistema está migrando desde una base de datos local con XAMPP/MySQL hacia **Supabase**, lo que implica cambios en la forma de conectarse, consultar, insertar y actualizar datos.

---

## 2.2. Dependencias externas identificadas

### Dependencia 1 — Supabase Database

Supabase se utilizará como base de datos del sistema.

El sistema depende de Supabase para:

- Consultar productos.
- Registrar productos.
- Actualizar stock.
- Registrar movimientos de entrada y salida.
- Guardar alertas de stock bajo.
- Consultar productos a reponer.

Esta dependencia debe probarse con cuidado porque cualquier error en la comunicación con la base de datos puede afectar directamente la integridad del inventario.

---

### Dependencia 2 — Supabase Auth

Supabase Auth puede utilizarse para gestionar la autenticación de usuarios.

El sistema depende del servicio de autenticación para:

- Iniciar sesión.
- Identificar al usuario.
- Controlar permisos según rol.
- Diferenciar acciones permitidas para empleado y encargado.

Este punto es importante porque ciertas funcionalidades, como importar Excel de proveedores o modificar stock, no deberían estar disponibles para cualquier usuario.

---

### Dependencia 3 — Archivos Excel de proveedores

El sistema también depende de archivos externos enviados por proveedores.

Estos archivos pueden contener:

- Nombre del proveedor.
- Fecha.
- Producto.
- Cantidad.
- Precio unitario.
- Total.

La importación de Excel es una funcionalidad crítica porque puede modificar muchas cantidades de stock en una sola operación.

---

## 2.3. Uso de mocks y stubs

Para probar la integración sin depender de Supabase real, se utilizarán **mocks** y **stubs**.

Un **mock** simula el comportamiento de una dependencia externa y permite verificar si fue llamada correctamente.

Un **stub** devuelve respuestas predefinidas para probar un flujo específico.

Esto permite:

- Evitar modificar datos reales.
- Probar errores controlados.
- Simular respuestas de Supabase.
- Validar el comportamiento del sistema aunque la base de datos externa no esté disponible.
- Ejecutar pruebas más rápido y con resultados repetibles.

---

## 2.4. Ejemplo de prueba de integración

### Caso: registrar una entrada de stock

El flujo esperado es:

1. El sistema consulta un producto existente en Supabase.
2. El sistema calcula el nuevo stock.
3. El sistema actualiza el stock en la base de datos.
4. El sistema registra el movimiento.
5. Si corresponde, actualiza o resuelve alertas.

---

## 2.5. Pseudocódigo de prueba de integración

```python
from unittest.mock import Mock
from services.stock_service import calcular_nuevo_stock


def registrar_movimiento_stock(db, producto_id, tipo, cantidad):
    producto = db.obtener_producto(producto_id)

    nuevo_stock = calcular_nuevo_stock(
        producto["stock_actual"],
        tipo,
        cantidad
    )

    db.actualizar_stock(producto_id, nuevo_stock)
    db.registrar_movimiento(producto_id, tipo, cantidad)

    return nuevo_stock


def test_registra_entrada_de_stock_con_mock_de_base_de_datos():
    db_mock = Mock()

    db_mock.obtener_producto.return_value = {
        "id": 1,
        "nombre": "Martillo",
        "stock_actual": 10
    }

    nuevo_stock = registrar_movimiento_stock(
        db=db_mock,
        producto_id=1,
        tipo="entrada",
        cantidad=5
    )

    assert nuevo_stock == 15
    db_mock.actualizar_stock.assert_called_once_with(1, 15)
    db_mock.registrar_movimiento.assert_called_once_with(1, "entrada", 5)
```

---

## 2.6. Herramientas recomendadas para integración

Se recomienda utilizar:

- **pytest**
- **unittest.mock**
- **pytest-mock**

### Justificación

Estas herramientas son gratuitas y adecuadas para la pila tecnológica del proyecto porque:

- Funcionan directamente con Python.
- Permiten simular Supabase sin conectarse realmente.
- Permiten validar que las funciones externas fueron llamadas correctamente.
- Son simples de integrar en un proyecto Flask.
- Facilitan pruebas durante la migración desde MySQL/XAMPP hacia Supabase.

---

## 2.7. Ubicación sugerida en el repositorio

```text
scr/ferreteria/tests/integration/test_stock_integration.py
scr/ferreteria/tests/mocks/
```

---

# 3. Pruebas de Componentes y de Sistema

## 3.1. Pruebas de componentes

### Componente seleccionado

Se selecciona como componente significativo:

**Módulo de gestión de stock**

Este componente es más grande que una función individual, pero no abarca todo el sistema.

Incluye:

- Consulta de productos.
- Registro de productos.
- Registro de entradas de stock.
- Registro de salidas de stock.
- Actualización de cantidades.
- Generación de alertas por stock bajo.
- Importación de Excel de proveedores.

---

## 3.2. Prueba del componente de forma aislada

El módulo de gestión de stock puede probarse de forma aislada utilizando una base de datos de prueba o mocks de Supabase.

### Entradas

- Producto existente.
- Stock actual.
- Stock mínimo.
- Tipo de movimiento: entrada, salida o ajuste.
- Cantidad del movimiento.
- Motivo del movimiento.
- Usuario que realiza la acción.

---

### Salidas esperadas

El componente debe:

- Actualizar correctamente el stock.
- Registrar el movimiento.
- Rechazar salidas inválidas.
- Generar una alerta si el stock queda por debajo del mínimo.
- Resolver o mantener alertas según corresponda.
- Mantener trazabilidad del usuario que realizó la operación.

---

## 3.3. Caso de prueba de componente

### Caso: salida de stock que genera alerta

**Datos iniciales:**

```text
Producto: Martillo
Stock actual: 6
Stock mínimo: 5
Salida solicitada: 3
```

**Resultado esperado:**

```text
Nuevo stock: 3
Movimiento registrado: salida
Alerta generada: stock bajo
```

**Validaciones:**

- El producto queda con stock actualizado en 3.
- Se guarda un movimiento de tipo salida.
- El motivo queda registrado.
- El sistema genera una alerta porque `3 < 5`.

---

## 3.4. Pruebas de sistema

Las pruebas de sistema validan el comportamiento completo de la aplicación desde la perspectiva del usuario.

En este proyecto, un flujo crítico es:

**Importar archivo Excel de proveedor para actualizar stock**

Este flujo es relevante porque involucra varias partes del sistema:

- Login.
- Control de permisos.
- Carga de archivo.
- Lectura de Excel.
- Actualización de stock.
- Registro de movimientos.
- Actualización de alertas.

---

## 3.5. Camino feliz: importar Excel de proveedor

### Paso 1 — Inicio de sesión

El usuario ingresa con credenciales válidas.

**Validaciones:**

- El login es exitoso.
- El sistema redirige al dashboard.
- Se muestra el nombre del usuario autenticado.

---

### Paso 2 — Acceso al módulo de importación

El usuario accede a la opción de importar Excel de proveedor.

**Validaciones:**

- La pantalla carga correctamente.
- Se muestra el formulario de carga.
- Solo el usuario autorizado puede acceder.

---

### Paso 3 — Carga del archivo Excel

El usuario selecciona un archivo `.xlsx` con el formato esperado:

```text
Proveedor | Fecha | Producto | Cantidad | Precio Unitario | Total
```

**Validaciones:**

- El sistema acepta archivos `.xlsx`.
- El sistema rechaza archivos con otro formato.
- El archivo puede leerse correctamente.

---

### Paso 4 — Procesamiento del archivo

El sistema procesa cada fila del Excel.

**Validaciones:**

- Si el producto existe, se actualiza el stock.
- Si el producto no existe, se informa como advertencia.
- Si la cantidad es inválida, no se actualiza el producto.
- No se interrumpe todo el proceso por un solo producto incorrecto.

---

### Paso 5 — Registro de movimientos

Por cada producto actualizado, se registra un movimiento de entrada.

**Validaciones:**

- El movimiento queda guardado.
- El tipo de movimiento es `entrada`.
- El motivo incluye el nombre del proveedor.
- El movimiento queda asociado al usuario que realizó la importación.

---

### Paso 6 — Verificación final

El usuario consulta el inventario actualizado.

**Validaciones:**

- El stock refleja las cantidades importadas.
- Los movimientos aparecen en el historial.
- Las alertas se actualizan correctamente.

---

## 3.6. Herramientas End-to-End evaluadas

### Cypress

Cypress es una herramienta moderna para automatizar pruebas en aplicaciones web.

**Ventajas:**

- Fácil de configurar.
- Buena experiencia visual.
- Útil para probar formularios y navegación.
- Sintaxis clara.

**Desventajas:**

- Tiene menor cobertura multi-navegador que Playwright.
- Puede ser menos flexible para escenarios más complejos.

---

### Playwright

Playwright es una herramienta moderna de automatización E2E desarrollada por Microsoft.

**Ventajas:**

- Soporta Chromium, Firefox y WebKit.
- Es rápido y estable.
- Permite probar flujos completos de usuario.
- Funciona bien con aplicaciones web modernas.
- Permite simular carga de archivos.

**Desventajas:**

- Puede requerir una configuración inicial un poco mayor que Cypress.

---

### Selenium

Selenium es una herramienta clásica de automatización de navegadores.

**Ventajas:**

- Muy flexible.
- Compatible con muchos lenguajes.
- Muy conocido en la industria.

**Desventajas:**

- Más complejo de configurar.
- Más verboso.
- Menos práctico para un proyecto académico pequeño o mediano.

---

### Herramienta E2E elegida

Se recomienda utilizar **Playwright**.

#### Justificación

Playwright es la herramienta más adecuada para este proyecto porque permite automatizar flujos completos como:

- Login.
- Navegación al dashboard.
- Consulta de productos.
- Registro de movimientos.
- Importación de archivos Excel.
- Verificación de resultados en pantalla.

Además, permite probar la aplicación en distintos navegadores y simular interacciones reales del usuario, incluyendo carga de archivos. Esto es útil para validar el flujo crítico de importación de Excel de proveedores.

---

# 4. Estrategia de regresión automatizada

Aunque la consigna principal se enfoca en pruebas unitarias, integración, componentes y sistema, se considera importante planificar pruebas de regresión.

Las pruebas de regresión permiten verificar que los cambios realizados en el sistema no rompan funcionalidades ya implementadas.

Esto es especialmente importante en este proyecto porque se está realizando una migración desde XAMPP/MySQL hacia Supabase.

---

## 4.1. Herramienta recomendada

**GitHub Actions**

### Justificación

GitHub Actions es gratuito para repositorios públicos y permite ejecutar pruebas automáticamente cada vez que se suben cambios al repositorio.

---

## 4.2. Workflow propuesto

```text
.github/workflows/test.yml
```

---

## 4.3. Activación

El workflow debería ejecutarse en:

- cada `push` hacia la rama principal
- cada `pull request`

---

## 4.4. Pruebas a ejecutar

Inicialmente:

```text
pytest
```

A futuro:

```text
pytest
playwright test
```

---

# 5. Pruebas de estrés planificadas

Las pruebas de estrés no son prioritarias en la etapa actual, pero se planifican para una fase posterior.

El objetivo será evaluar el comportamiento del sistema ante muchas operaciones simultáneas.

---

## 5.1. Escenario propuesto

Simular múltiples consultas y movimientos de stock al mismo tiempo.

Ejemplo:

```text
500 consultas de productos en pocos minutos
100 registros de movimientos de stock simultáneos
50 importaciones de Excel en un período corto
```

---

## 5.2. Herramienta recomendada

Se recomienda utilizar **Locust**.

### Justificación

Locust es una herramienta gratuita escrita en Python, por lo que se adapta bien al stack del proyecto. Permite simular usuarios concurrentes y medir tiempos de respuesta en endpoints del sistema.

---

# 6. Resumen de herramientas elegidas

| Nivel de prueba | Herramienta | Uso en el proyecto | Justificación |
|----------------|-------------|-------------------|---------------|
| Unitarias | pytest | Validar reglas de negocio como stock suficiente | Compatible con Flask y simple de usar |
| Integración | unittest.mock / pytest-mock | Simular Supabase y autenticación | Permite aislar dependencias externas |
| Componentes | pytest + mocks | Probar módulo de gestión de stock | Valida comportamiento del módulo sin depender de servicios reales |
| Sistema / E2E | Playwright | Automatizar flujos completos de usuario | Soporta navegación, formularios y carga de archivos |
| Regresión | GitHub Actions | Ejecutar pruebas automáticamente | Gratuito e integrado con GitHub |
| Estrés | Locust | Simular carga futura | Compatible con Python y útil para endpoints |

---

# Conclusión

La estrategia de pruebas propuesta permite validar el sistema en distintos niveles.

Las pruebas unitarias verifican reglas críticas de negocio, como evitar salidas de stock inválidas. Las pruebas de integración permiten comprobar la comunicación con servicios externos, especialmente Supabase, sin depender de datos reales. Las pruebas de componentes validan módulos más completos, como la gestión de stock, mientras que las pruebas de sistema permiten comprobar flujos completos desde la perspectiva del usuario.

Además, se contempla una estrategia de regresión automatizada con GitHub Actions y una planificación futura de pruebas de estrés con Locust.

Este enfoque permite mejorar la confiabilidad del sistema, reducir errores durante la migración a Supabase y asegurar que las funcionalidades principales sigan funcionando correctamente a medida que el proyecto evoluciona.
