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

# B1. Pruebas Unitarias

## Módulo o función seleccionada

Se selecciona como función concreta a probar:

**Validar salida de stock**

Esta función representa una regla crítica del sistema: no se debe permitir registrar una salida de stock si la cantidad solicitada es mayor al stock disponible.

La regla de negocio es:

> El sistema debe rechazar cualquier salida de stock que genere valores negativos en el inventario.

Esta validación es importante porque el stock es el dato central del sistema. Si el sistema permite stock negativo, la información del inventario deja de ser confiable y puede afectar decisiones de compra, ventas y reposición.

---

## Parámetros de entrada

La función recibe dos parámetros principales:

| Parámetro | Tipo esperado | Descripción |
|----------|--------------|-------------|
| `stock_actual` | Entero | Cantidad disponible actualmente del producto |
| `cantidad_salida` | Entero | Cantidad que se desea retirar del stock |

---

## Clases de equivalencia

Las clases de equivalencia permiten agrupar entradas que deberían producir el mismo comportamiento del sistema.

### validar_salida_stock – Técnica: partición de equivalencia

| ID   | Método/Función                 | Técnica        | Datos de entrada               | Resultado esperado |
|------|--------------------------------|----------------|--------------------------------|--------------------|
| UT01 | `validar_salida_stock`         | Equivalencia   | `stock_actual=10, cantidad_salida=5`   | `True`             |
| UT02 | `validar_salida_stock`         | Equivalencia   | `stock_actual=10, cantidad_salida=15`  | `False`            |
| UT03 | `validar_salida_stock`         | Equivalencia   | `stock_actual=10, cantidad_salida=0`   | `False`            |

**Justificación de las clases:**  
- UT01 representa la clase válida (salida menor al stock).  
- UT02 representa la clase inválida (salida mayor al stock).  
- UT03 representa otra clase inválida (cantidad cero).

## Cómo se aplica para diseñar casos de prueba
En la práctica, esta técnica se aplica identificando todas las condiciones posibles (válidas e inválidas) y seleccionando un único valor representativo de cada clase para construir un caso de prueba. La premisa es que si el sistema procesa correctamente ese valor, procesará igual de bien cualquier otro valor que pertenezca a la misma clase. Esto permite reducir drásticamente la cantidad total de pruebas a ejecutar sin perder cobertura. Por ejemplo, en un sistema de gestión de inventario, si extraer 5 unidades de un stock de 10 funciona correctamente (clase válida), se asume que no es necesario diseñar pruebas adicionales para extraer 3, 4 o 6 unidades; un solo caso es suficiente para validar toda la condición.

---

## Valores límite

Un valor límite es aquel dato o entrada que se encuentra exactamente en las fronteras o extremos de una clase de equivalencia. Esto incluye los valores máximos y mínimos permitidos, así como los valores inmediatamente adyacentes a esas fronteras (justo por debajo del mínimo o justo por encima del máximo).

### validar_cantidad_positiva – Técnica: valores límite

| ID   | Método/Función                 | Técnica          | Datos de entrada  | Resultado esperado |
|------|--------------------------------|------------------|-------------------|--------------------|
| UT04 | `validar_cantidad_positiva`    | Valor límite     | `cantidad=0`      | `False`            |
| UT05 | `validar_cantidad_positiva`    | Valor límite     | `cantidad=-1`     | `False`            |
| UT06 | `validar_cantidad_positiva`    | Valor límite     | `cantidad=1`      | `True`             |

**Justificación de los límites:**  
El límite crítico es el 0, donde la función cambia de inválido a válido.  
- 0 está exactamente en el límite y debe ser rechazado.  
- -1 es el entero inmediatamente inferior al límite (rechazado).  
- 1 es el primer valor positivo después del límite (aceptado).  
Estos tres valores cubren las fronteras y detectan errores como `>=` en lugar de `>`.

## Cómo se aplica para encontrar defectos
Se aplica dirigiendo los casos de prueba específicamente a estas fronteras, ya que la experiencia demuestra que la mayoría de los defectos lógicos ocurren en los bordes de las condiciones. Al probar los límites, se busca identificar errores comunes de programación, como el uso incorrecto de operadores relacionales (por ejemplo, usar < en lugar de <=) o los errores de "desplazamiento por uno" (off-by-one errors). Al forzar al sistema a procesar el límite exacto (ej. solicitar 10 unidades cuando el stock es 10) y el primer valor inválido (solicitar 11), los defectos en la lógica condicional quedan expuestos de forma inmediata.

---

# B2. Framework de pruebas y automatización CI/CD

## Framework elegido

Se seleccionó **pytest** como framework de pruebas unitarias para el proyecto **FerreteriaStock**.

**Justificación**:
- Es gratuito y compatible con Python/Flask (stack tecnológico del sistema).
- Sintaxis sencilla con `assert`, reduciendo la complejidad de las pruebas.
- Excelente integración con `unittest.mock` para simular servicios externos como Supabase.
- Rápido en ejecución (6 pruebas en 0.02s), adecuado para pipelines CI/CD.
- Ampliamente documentado y usado en la industria, lo que facilita el mantenimiento.

## Pipeline CI/CD con GitHub Actions

Se configuró un archivo `.github/workflows/test.yml` que ejecuta automáticamente las pruebas unitarias en cada `push` y `pull request` a las ramas principales (`main`/`master`).

El pipeline realiza los siguientes pasos:
1. Checkout del repositorio.
2. Configuración de Python 3.13.
3. Instalación de dependencias (pytest).
4. Ejecución de las pruebas con `pytest tests/unit/ --verbose`.

**Resultado esperado**: los tests deben aparecer en verde en la consola de GitHub Actions, proporcionando una validación continua de la integridad del código.

## Evidencia

- **Captura de pantalla**:  
  ![Pipeline CI/CD exitoso](https://github.com/user-attachments/assets/b45a05e4-d2c3-43f2-84a7-ed69b76bf1e3)

- **Video demostrativo**:  
  [https://youtu.be/sWL_zxhJF9s](https://youtu.be/sWL_zxhJF9s)

---

# B3. Pruebas de Integración

## Objetivo

Las pruebas de integración verifican que distintos módulos del sistema funcionen correctamente en conjunto.

En este proyecto, son especialmente importantes porque el sistema está migrando desde una base de datos local con XAMPP/MySQL hacia **Supabase**, lo que implica cambios en la forma de conectarse, consultar, insertar y actualizar datos.

---

## Dependencias externas identificadas

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

## Uso de mocks y stubs

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

## Ejemplo de prueba de integración

### Caso: registrar una entrada de stock

El flujo esperado es:

1. El sistema consulta un producto existente en Supabase.
2. El sistema calcula el nuevo stock.
3. El sistema actualiza el stock en la base de datos.
4. El sistema registra el movimiento.
5. Si corresponde, actualiza o resuelve alertas.

---

## Pseudocódigo de prueba de integración

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
