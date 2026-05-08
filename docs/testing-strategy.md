## B3. Diseño conceptual de pruebas de integración

### a. Identificación de dos dependencias externas

Para que las pruebas de integración sean efectivas es necesario identificar los componentes que están fuera del control directo de las funciones escritas en Python y cuya falla o ausencia impediría ejecutar el flujo completo. Se han detectado dos dependencias críticas:

**1. Motor de base de datos relacional (MySQL/MariaDB)**  
- **Naturaleza:** infraestructura externa que se comunica con la aplicación mediante TCP/IP (red o sockets locales).  
- **Impacto en la integración:** el sistema de la ferretería depende de la disponibilidad del servidor, de la integridad del esquema (tablas `productos`, `usuarios`, `movimientos_stock`) y de la persistencia de los datos. Una prueba de integración no solo verifica que el código Python sea correcto, sino que las sentencias SQL (por ejemplo, el cálculo de stock en `registrar_movimiento`) interactúan correctamente con las restricciones y los tipos de datos definidos en el motor.

**2. Sistema de archivos y persistencia en disco (módulo `os` y directorio `uploads`)**  
- **Naturaleza:** dependencia del sistema operativo que gestiona la lectura y escritura de archivos físicos.  
- **Impacto en la integración:** la función de importación de Excel utiliza la librería `openpyxl` para leer documentos guardados en la carpeta `uploads`. La prueba de integración debe validar que la aplicación tenga los permisos de escritura necesarios, que el archivo se guarde correctamente después de la subida y que sea eliminado (limpieza de temporales) una vez procesado el Excel del proveedor.

### b. Explicación de cómo se mockearían/stubearían en una prueba futura

**¿Qué significa «mockear» en las pruebas de software?**  
El término *mock* (simular, imitar) designa una técnica fundamental en control de calidad: reemplazar dependencias externas reales —bases de datos, APIs de terceros, red, sistema de archivos— por objetos simulados y controlados durante la ejecución de pruebas automatizadas.

En las pruebas de integración a menudo necesitamos aislar la aplicación para no depender de la infraestructura externa (por ejemplo, evitar levantar un servidor MySQL real en cada ejecución de GitHub Actions). El objetivo de estos *dobles de prueba* es garantizar tres propiedades clave:

- **Determinismo:** el resultado siempre es el mismo, ya que no está sujeto al estado cambiante de una base de datos o de la red.  
- **Velocidad:** se elimina la sobrecarga de tiempo que implica iniciar infraestructura real o realizar operaciones pesadas de entrada/salida (E/S).  
- **Independencia:** se prueba la lógica de negocio sin riesgo de que factores externos (servidor caído, falta de permisos en disco) generen falsos negativos.

A partir de este concepto se emplean dos enfoques distintos según lo que se desee evaluar:

**1. Stubbing de la base de datos (pruebas basadas en estado)**  
- **Concepto:** un *Stub* es un objeto que devuelve respuestas predefinidas (*enlatadas*) a las llamadas que se realizan durante la prueba. Sirve para simular el estado del sistema.  
- **Aplicación:** para probar la ruta `/productos`, en lugar de consultar la base real, se *stubea* la función `get_db_connection()`. Cuando el código solicita la lista de productos, el Stub devuelve un diccionario estático como:  
  ```python
  [{'id': 1, 'nombre': 'Martillo', 'stock_actual': 5, 'stock_minimo': 10}]
  ```  
  Esto permite verificar que el frontend y la lógica de Python procesan y muestran correctamente los datos, sin depender de que la base esté vacía o caída.

**2. Mocking de componentes de entrada/salida (pruebas basadas en interacción)**  
- **Concepto:** un *Mock* es un objeto más complejo que no solo devuelve datos, sino que registra cómo fue invocado (cuántas veces, con qué argumentos, en qué orden). Se utiliza para verificar el comportamiento y la interacción entre componentes.  
- **Aplicación:** al probar la carga de facturas de proveedores, se *mockea* el objeto `request.files['archivo']`. No hace falta un archivo `.xlsx` real en disco. El Mock verificará que la función `importar()` llame efectivamente al método `.save()` con la ruta de destino correcta. Si el método no se invoca, el Mock hace que la prueba falle, garantizando que la integración con el sistema de archivos se comporte según lo esperado.

### c. Ejemplo de flujo de prueba de integración

Tomaremos el flujo **«Registro de salida de stock con disparo de alerta»**, uno de los procesos más críticos del sistema, porque integra la lógica de control, el estado de la base de datos y el sistema interno de notificaciones.

**Escenario de prueba:** registro de una venta que deja el producto por debajo del stock mínimo.  

- **Precondición (Setup):** se utiliza un Stub para simular la respuesta de la base de datos.  
  El Stub devuelve un producto *Pinza de Presión* con `id=10`, `stock_actual=5` y `stock_minimo=4`.

- **Ejecución (Stimulus):** se realiza una petición simulada (usando el cliente de pruebas de Flask) a la ruta `POST /movimientos/registrar` con los siguientes datos:  
  `id_producto=10`, `tipo='salida'`, `cantidad=2`, `motivo='Venta mostrador'`.

- **Lógica de integración (Procesamiento):**  
  1. El sistema calcula el nuevo stock: `5 - 2 = 3`.  
  2. Detecta que `3 < 4` (stock mínimo) y debe disparar la creación de una alerta.

- **Verificación (Assertion):**  
  - Se comprueba que se haya llamado al método `execute` del cursor de la base de datos para realizar el `UPDATE` en la tabla `productos` con el valor `3`.  
  - Se verifica (a través del Mock) que se haya ejecutado una sentencia `INSERT INTO alertas` con el mensaje de stock bajo correspondiente.  
  - Se comprueba que la respuesta del servidor sea una redirección (`302 Redirect`) hacia la página de movimientos.

- **Limpieza (Teardown):** se resetean los objetos Mock para asegurar que la siguiente prueba sea independiente.

### d. Recomendación de una herramienta para dobles de prueba

**Herramienta recomendada:** `unittest.mock` (módulo oficial de la biblioteca estándar de Python) en combinación con `pytest`.

**Justificación técnica:**  
- **Nativa y ligera:** al formar parte de la biblioteca estándar, no añade dependencias externas pesadas al proyecto, facilita la portabilidad del código y garantiza la compatibilidad en entornos de CI/CD como GitHub Actions.  
- **Flexibilidad de objetos:** permite crear `MagicMock`, un tipo de objeto «todoterreno» capaz de imitar cualquier método o atributo (como `.execute()`, `.fetchone()` o `.commit()` de la conexión a MySQL) de forma dinámica.  
- **Aislamiento total:** la función `patch()` posibilita interceptar `get_db_connection` en `app.py`. Así se «engaña» a la aplicación para que use una conexión simulada durante los tests, logrando que las pruebas sean rápidas, no requieran un servidor MySQL real encendido y no alteren los datos de producción.

---

# Testing Strategy — Stockeado  
## Estrategia Integral de Pruebas del Sistema

### 1. Introducción

Este documento consolida la estrategia completa de pruebas del proyecto **Stockeado**, integrando la investigación previa (B0), los casos de prueba unitaria (Parte B), la discusión del foro y la planificación de pruebas futuras. El objetivo es garantizar que el sistema funcione correctamente en todos sus módulos, con trazabilidad de errores y un proceso de verificación repetible.

**Stack tecnológico bajo prueba:**  
- Backend: Python 3.12 + Flask  
- Frontend: HTML/CSS/JS con Jinja2  
- Base de datos: MySQL (XAMPP)  
- Patrones probados: Observer (alertas), Strategy (movimientos)

---

### 2. Tabla de herramientas de testing

| Herramienta      | Categoría           | Instalación             | Uso en el proyecto |
|------------------|---------------------|--------------------------|---------------------|
| `pytest`         | Framework de pruebas| `pip install pytest`     | Framework principal para todas las pruebas unitarias e integración |
| `unittest`       | Framework de pruebas| Incluido en Python       | Base para clases de mock |
| `unittest.mock`  | Mocking             | Incluido en Python       | Simular conexiones MySQL sin base de datos real |
| Flask test client| Cliente HTTP        | Incluido en Flask        | Pruebas de rutas, sesiones y respuestas HTTP |
| `pytest-cov`     | Cobertura           | `pip install pytest-cov` | Medir porcentaje de cobertura del código |
| Playwright       | E2E (futuro)        | `pip install playwright` | Pruebas End-to-End automatizadas en el navegador |
| Locust           | Estrés (futuro)     | `pip install locust`     | Pruebas de carga y estrés |
| `pytest-html`    | Reportes            | `pip install pytest-html`| Generar reportes HTML de resultados |

---

### 3. Pirámide de testing del proyecto

```
             /\
          /E2E\         ← Pocos, lentos, cobertura de flujos completos
       /──────\
      / Integr  \       ← Rutas Flask con DB en memoria / mocks
     /──────────\
    / Unitarias   \     ← Muchos, rápidos, lógica de negocio aislada
   /──────────────\
```

**Distribución planificada:**  
- 70% Pruebas unitarias (lógica de negocio, validaciones)  
- 20% Pruebas de integración (rutas HTTP con mocks de DB)  
- 10% Pruebas E2E (flujos completos en navegador)

---

### 4. Casos de prueba de ejemplo

#### 4.1 Flujo de Login (integración)

```python
# CASO: Login exitoso redirige al dashboard según rol
def test_login_redirige_segun_rol():
    # Encargado → dashboard
    # Empleado → dashboard (acceso diferenciado por controles en templates)
    pass

# CASO: Login fallido no crea sesión
def test_login_fallido_sin_sesion():
    pass

# CASO: Usuario inactivo (activo=0) no puede loguear
def test_usuario_inactivo_rechazado():
    pass
```

#### 4.2 Control de Stock (unitarias)

```python
# Clase: EstrategiaEntrada
# Método: ejecutar(producto, cantidad)
# Caso 1: stock_actual += cantidad → correcto
# Caso 2: cantidad = 0 → rechazado
# Caso 3: cantidad negativa → rechazado

# Clase: EstrategiaSalida
# Caso 1: stock_actual > cantidad → salida exitosa
# Caso 2: stock_actual == cantidad → stock queda en 0
# Caso 3: stock_actual < cantidad → rechazado con error

# Clase: EstrategiaAjuste
# Caso 1: cantidad = 0 → stock queda en 0
# Caso 2: cantidad > stock_minimo → no genera alerta
# Caso 3: cantidad < stock_minimo → genera alerta
```

#### 4.3 Observer de Alertas (unitarias)

```python
# Clase: ObservadorStock
# Caso 1: stock_actual < stock_minimo → INSERT en alertas
# Caso 2: alerta ya existe (resuelta=0) → no duplicar
# Caso 3: stock_actual >= stock_minimo → UPDATE resuelta=1
# Caso 4: stock_actual = stock_minimo (límite exacto) → sin alerta
```

#### 4.4 Importación de Excel

```python
# Caso 1: Fila válida → producto actualizado, movimiento registrado
# Caso 2: Producto no encontrado en DB → advertencia, sin error fatal
# Caso 3: Cantidad = 0 en Excel → fila ignorada
# Caso 4: Celda vacía → fila ignorada sin crash
# Caso 5: Stock recupera mínimo → alerta resuelta automáticamente
```

---

### 5. Plan de Mocks

Los mocks permiten ejecutar las pruebas sin depender de una instancia real de MySQL, lo que las hace más rápidas, repetibles y aisladas.

#### 5.1 Mock de conexión a base de datos

```python
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_db():
    with patch('app.get_db_connection') as mock_conn:
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value = conn
        yield conn
```

| Componente           | Mock               | Propósito |
|----------------------|--------------------|-----------|
| `get_db_connection()`| `MagicMock()`      | Evitar conexión real a MySQL |
| `cursor.fetchone()`  | Retorna dict configurado | Simular resultado de SELECT |
| `cursor.fetchall()`  | Retorna lista de dicts | Simular listados |
| `cursor.execute()`   | Registra llamadas  | Verificar que se ejecutaron los SQL correctos |
| `conn.commit()`      | Registra llamadas  | Verificar que se confirmaron transacciones |

#### 5.2 Mock de sesiones Flask

```python
@pytest.fixture
def sesion_encargado(client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = 1
        sess['nombre'] = 'Encargado'
        sess['rol'] = 'encargado'

@pytest.fixture
def sesion_empleado(client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = 2
        sess['nombre'] = 'Juan Empleado'
        sess['rol'] = 'empleado'
```

#### 5.3 Mock de archivo Excel

```python
import openpyxl
import io

def crear_excel_mock(filas):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Proveedor', 'Fecha', 'Producto', 'Cantidad', 'Precio'])
    for fila in filas:
        ws.append(fila)
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

# Uso en test:
excel_data = crear_excel_mock([
    ['Distribuidora del Norte', '2026-05-01', 'Martillo 500g', 10, 2500]
])
```

---

### 6. Flujo E2E básico

El flujo End-to-End más crítico del sistema es el ciclo completo de gestión de stock, desde el login hasta la resolución de una alerta.

**Flujo E2E: Ciclo de Stock Bajo → Alerta → Reposición**

```
[1] Usuario accede a /login
     └── Ingresa email + password de empleado
     └── Sistema valida credenciales en DB
     └── Redirige a /dashboard

[2] Dashboard muestra estado actual
     └── Métricas cargadas desde DB (productos, alertas, movimientos)

[3] Empleado registra una salida de stock
     └── Accede a /movimientos/nuevo
     └── Selecciona producto, tipo=salida, cantidad, motivo
     └── Sistema aplica EstrategiaSalida
     └── stock_actual se actualiza en DB
     └── Si stock_actual < stock_minimo → Observer genera alerta

[4] Encargado ve la alerta
     └── Accede a /alertas
     └── Ve alerta con badge rojo "Stock bajo"
     └── Accede a /reposicion para ver cantidad sugerida

[5] Empleado importa Excel del proveedor
     └── Accede a /importar
     └── Sube archivo .xlsx
     └── Sistema procesa filas, actualiza stock
     └── Si stock_actual >= stock_minimo → Observer resuelve alerta

[6] Dashboard refleja nuevo estado
     └── Alerta desaparece del contador
     └── Stock del producto normalizado
```

**Script E2E con Playwright (futuro)**

```python
from playwright.sync_api import sync_playwright

def test_ciclo_stock_completo():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Login
        page.goto('http://localhost:5000')
        page.fill('input[name=email]', 'juan@ferreteria.com')
        page.fill('input[name=password]', 'emp123')
        page.click('button[type=submit]')
        page.wait_for_url('**/dashboard')

        # Registrar salida
        page.goto('http://localhost:5000/movimientos/nuevo')
        page.select_option('select[name=tipo]', 'salida')
        page.select_option('select[name=id_producto]', '5')  # Llave de paso
        page.fill('input[name=cantidad]', '3')
        page.fill('input[name=motivo]', 'Prueba E2E')
        page.click('button[type=submit]')

        # Verificar alerta generada
        page.goto('http://localhost:5000/alertas')
        assert page.locator('.badge-danger').count() > 0

        browser.close()
```

---

### 7. Estrategia de Regresión

Las pruebas de regresión garantizan que los cambios en el código no rompan funcionalidades ya implementadas.

#### 7.1 Cuándo ejecutar regresión

| Evento                          | Tipo de regresión                               |
|---------------------------------|-------------------------------------------------|
| Merge a `main`                  | Suite completa                                  |
| Nueva funcionalidad implementada| Suite del módulo afectado + módulos relacionados|
| Corrección de bug               | Test específico del bug + suite del módulo      |
| Cambio en DB (nueva columna, relación) | Suite completa + pruebas de integridad   |
| Cambio en lógica de stock       | TC-STOCK-* + TC-ALERTA-* obligatoriamente       |

#### 7.2 Suite de Regresión Core

Los siguientes casos son obligatorios en toda regresión, por cubrir la lógica de negocio crítica:

- **TC-AUTH-001** — Login válido  
- **TC-AUTH-003** — Acceso sin sesión  
- **TC-STOCK-001** — Entrada de stock  
- **TC-STOCK-002** — Salida rechazada por insuficiencia  
- **TC-ALERTA-001** — Generación automática de alerta  
- **TC-ALERTA-002** — No duplicación de alertas  
- **TC-PROD-002** — Borrado lógico (no DELETE)

#### 7.3 Proceso de Regresión

```bash
# Ejecutar suite de regresión core
pytest tests/ -m "regresion" -v --tb=short

# Ejecutar con reporte
pytest tests/ -m "regresion" --html=reports/regresion_$(date +%Y%m%d).html

# Revisar cobertura post-regresión
pytest tests/ --cov=app --cov-report=html
```

#### 7.4 Registro de Regresiones

Cada regresión debe quedar documentada en el historial del repositorio con:

- Fecha y versión (commit SHA)  
- Casos ejecutados  
- Resultados (PASS/FAIL por caso)  
- Bugs encontrados y tickets abiertos

---

### 8. Plan de Estrés Futuro

El plan de estrés está previsto para la etapa final del proyecto (TP3), cuando el sistema esté completamente integrado.

#### 8.1 Herramienta: Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class UsuarioStockeado(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login al inicio de cada sesión de usuario"""
        self.client.post('/login', data={
            'email': 'juan@ferreteria.com',
            'password': 'emp123'
        })

    @task(3)
    def ver_dashboard(self):
        self.client.get('/dashboard')

    @task(2)
    def ver_productos(self):
        self.client.get('/productos')

    @task(1)
    def registrar_movimiento(self):
        self.client.post('/movimientos/nuevo', data={
            'tipo': 'entrada',
            'id_producto': 1,
            'cantidad': 1,
            'motivo': 'Test de carga'
        })

    @task(1)
    def ver_alertas(self):
        self.client.get('/alertas')

# Ejecutar prueba de carga
locust -f locustfile.py --host=http://localhost:5000 \
       --users 50 --spawn-rate 5 --run-time 60s
```

#### 8.2 Escenarios de estrés planificados

| Escenario               | Usuarios concurrentes | Duración | Métrica objetivo |
|-------------------------|------------------------|----------|-------------------|
| Carga normal            | 10 usuarios            | 5 min    | Respuesta < 500ms en 95% de requests |
| Carga media             | 25 usuarios            | 5 min    | Respuesta < 1000ms, sin errores 5xx |
| Carga alta              | 50 usuarios            | 2 min    | Sin crashes del servidor Flask |
| Pico de importación     | 5 usuarios simultáneos importando Excel | 1 min    | Sin corrupción de datos |
| Concurrencia en stock   | 10 usuarios registrando movimientos del mismo producto | 2 min    | Integridad del `stock_actual` |

#### 8.3 Métricas a monitorear

- Tiempo de respuesta promedio (target: < 500ms)  
- Percentil 95 de tiempo de respuesta  
- Tasa de error (target: 0% errores 5xx)  
- Throughput (requests por segundo)  
- Integridad del stock tras operaciones concurrentes

#### 8.4 Criterios de fallo

El sistema se considera fallido en la prueba de estrés si:

- Más del 1% de los requests retornan error 5xx.  
- El tiempo de respuesta p95 supera los 3 segundos.  
- La base de datos muestra inconsistencias de stock tras la prueba.  
- El servidor Flask se cae y requiere reinicio manual.

---
