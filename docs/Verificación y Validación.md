## --- SECCIÓN 1: Verificación vs Validación ---

**1. Verificación vs Validación**

La diferencia clave es el momento y el objetivo de cada actividad. La verificación responde a la pregunta "¿estamos construyendo el sistema correctamente?", mientras que la validación responde a "¿estamos construyendo el sistema correcto?". En otras palabras, la verificación controla que el producto cumpla con las especificaciones técnicas definidas, y la validación controla que el producto satisfaga las necesidades reales del usuario.

Ejemplo de verificación en el proyecto: revisar que la función `registrar_movimiento` en `app.py` aplique correctamente el patrón Strategy, es decir, que una entrada sume al stock, una salida lo reste y un ajuste establezca el valor exacto, tal como fue especificado en el diseño.

Ejemplo de validación en el proyecto: mostrarle al encargado de la ferretería el módulo de alertas y preguntarle si la información que muestra el sistema (producto con stock bajo, cantidad a reponer) le resulta suficiente para tomar la decisión de hacer un pedido al proveedor. Si el encargado dice que necesita también ver el nombre del proveedor habitual, eso es un hallazgo de validación.

---

**2. Planificación de V&V para el próximo sprint**

Las dos actividades concretas que incluiríamos son las siguientes.

La primera es una inspección de código del módulo de importación de Excel. Antes de dar por finalizada esa funcionalidad, el Dev Lead revisaría el código de la ruta `/importar` en `app.py` para verificar que el manejo de errores sea robusto, que no se procesen filas vacías, que el archivo se elimine correctamente después de procesarse y que los movimientos queden registrados con todos los campos requeridos (tipo, cantidad, motivo, usuario, fecha).

La segunda es una prueba funcional de extremo a extremo del flujo de reposición. Se ejecutaría manualmente el flujo completo: registrar una salida de stock que baje el producto por debajo del mínimo, verificar que se genere la alerta automáticamente, subir el Excel del proveedor con la cantidad correspondiente, y confirmar que el stock se actualice correctamente y la alerta quede resuelta. Este flujo cubre tres módulos del sistema de forma integrada.

---

**3. Inspección de código vs prueba automática**

Una inspección de código es una revisión manual realizada por uno o más integrantes del equipo que leen el código sin ejecutarlo. El objetivo es detectar problemas de diseño, lógica incorrecta, incumplimiento de estándares o código difícil de mantener. Una prueba automática, en cambio, ejecuta el código con entradas definidas y verifica que las salidas sean las esperadas, sin intervención humana.

La diferencia principal es que la inspección puede detectar problemas que una prueba no detecta, como código duplicado, decisiones de diseño incorrectas o ausencia de manejo de casos borde. La prueba automática, por su parte, puede ejecutarse cientos de veces sin esfuerzo humano y garantiza que el comportamiento no cambie con el tiempo.

Conviene más una inspección cuando el equipo está tomando decisiones de arquitectura o implementando un patrón de diseño por primera vez, como fue el caso de la implementación de Observer y Strategy en nuestro proyecto. Conviene más una prueba automática cuando se trata de funcionalidades críticas que deben verificarse después de cada cambio, como la lógica de actualización de stock.

---

**4. Análisis estático automatizado**

La herramienta que aplicaría directamente al proyecto es **Pylint**, que analiza código Python sin necesidad de ejecutarlo.

En el código del proyecto, Pylint podría detectar los siguientes tipos de errores. Variables definidas pero no utilizadas, como podría ocurrir si en alguna refactorización quedó una variable sin usar. Funciones con demasiada complejidad ciclomática, por ejemplo si la función `registrar_movimiento` creciera con más condiciones. Importaciones innecesarias o en orden incorrecto. Ausencia de docstrings en las funciones, lo cual afecta la mantenibilidad. Y acceso a variables que podrían no estar definidas en ciertos flujos de ejecución, como el caso de `nuevo_stock` dentro de la función `registrar_movimiento`, que solo se define si el tipo es entrada, salida o ajuste, y si llegara un tipo no contemplado quedaría indefinida.

Para ejecutarlo en el proyecto alcanza con correr en la terminal:

```
pylint app.py
```

---

**5. Métodos formales de verificación**

Los métodos formales son imprescindibles en sistemas donde un fallo puede tener consecuencias irreversibles o poner en riesgo vidas humanas. Los casos más claros son sistemas de control de aeronaves, software médico (como marcapasos o respiradores), sistemas de control nuclear, protocolos criptográficos y software de trenes o semáforos. En estos contextos no alcanza con probar que el sistema funciona en la mayoría de los casos, se necesita demostrar matemáticamente que no puede fallar bajo ninguna condición posible.

No se usan siempre porque tienen un costo altísimo en tiempo, conocimiento especializado y recursos. Requieren que los desarrolladores tengan formación en lógica matemática y lenguajes de especificación formal como Z, TLA+ o Alloy. Además, el esfuerzo de formalizar un sistema completo es desproporcionado para la mayoría de los proyectos comerciales donde un error tiene consecuencias manejables. En el caso del sistema de inventario de la ferretería, un error en el stock es grave pero no pone en riesgo vidas, por lo que los métodos formales no están justificados.

---

**6. Reuniones de validación en Scrum y el rol del Product Owner**

En una Sprint Review, el Product Owner cumple el rol de representar la voz del cliente y del negocio. Es quien evalúa si las funcionalidades desarrolladas durante el sprint cumplen con los criterios de aceptación definidos al inicio, y quien decide si cada ítem del backlog puede considerarse terminado o si requiere ajustes. No valida aspectos técnicos sino que valida que el sistema resuelve el problema del negocio de la manera esperada.

En el caso del proyecto, el Product Owner sería quien confirmaría, por ejemplo, que la pantalla de alertas muestra la información suficiente para que el encargado de la ferretería tome decisiones de reposición, o que el flujo de importación de Excel del proveedor funciona de forma comprensible para un usuario sin conocimientos técnicos.

La relación con las pruebas automatizadas es complementaria. Las pruebas automatizadas garantizan que el sistema funciona correctamente desde el punto de vista técnico antes de llegar a la Sprint Review, evitando que el Product Owner encuentre errores básicos durante la demostración. De esta forma, la Sprint Review puede enfocarse en la validación del negocio y no en la detección de bugs, que es responsabilidad del equipo técnico resolver antes de la reunión.

## --- SECCIÓN 2: Planificación de V&V (tabla) ---

Hemos completado la tabla para los próximos 2 sprints (cada sprint = 1 semana real):

| Sprint | Actividad de V&V | Técnica | Responsable | Herramienta |
| :--- | :--- | :--- | :--- | :--- |
| **Actual** | Análisis de calidad de código en `app.py` (variables sin usar, complejidad, docstrings). | Análisis estático automatizado | Dev Lead | Pylint |
| **Actual** | Verificación de la aplicación del patrón *Strategy* en `registrar_movimiento`. | Inspección de código / Revisión de diseño | Dev Lead | Revisión manual |
| **Próximo** | Inspección de código del módulo de importación de Excel (ruta `/importar` en `app.py`). | Inspección de código (manual) | Dev Lead | Checklist de revisión / IDE |
| **Próximo** | Prueba del flujo completo de reposición (alerta, subida de Excel, actualización de stock). | Prueba funcional de extremo a extremo (E2E) | QA / Tester | Ejecución manual |
| **Próximo** | Validación de la información del módulo de alertas con el encargado de la ferretería. | Validación con el usuario / Sprint Review | Product Owner | Entorno de Pruebas / Demo |

## --- SECCIÓN 3: Inspección y análisis estático ---

### a) ¿Qué archivo o módulo de su proyecto inspeccionarían primero? ¿Por qué?
El primer módulo a inspeccionar manualmente será la ruta `/importar` del archivo `app.py` (módulo de importación de Excel). 

**¿Por qué?** 1. **Criticidad y Riesgo:** Es un punto de entrada de datos externos masivos al sistema. Un fallo aquí puede corromper el inventario completo de la ferretería o registrar datos inconsistentes de golpe.
2. **Complejidad del Manejo de Errores:** Al procesar archivos de terceros, existen múltiples escenarios de fallo que el código debe prever (columnas vacías, formatos incorrectos, tipos de datos corruptos). 
3. **Manejo de Recursos:** Requiere asegurar que el archivo subido se elimine del servidor inmediatamente después de ser procesado para evitar saturación de almacenamiento. Una inspección manual del Dev Lead es ideal aquí para evaluar la robustez lógica antes de que pase a producción.

### b) Elijan una herramienta de análisis estático y digan qué regla aplicarían primero.
Utilizaremos **Pylint** (conforme a lo planificado para el Sprint Actual). La primera regla o categoría de mensajes que aplicaríamos de manera prioritaria es la de **Errores (E - Errors)**, específicamente la regla `used-before-assignment` (E0601) y `undefined-variable` (E0606).

**Justificación:** En nuestro archivo `app.py`, dentro de la función `registrar_movimiento`, la variable `nuevo_stock` se calcula de forma dinámica dependiendo del tipo de movimiento (entrada, salida o ajuste). Si ingresara un tipo no contemplado o si ocurriese una falla en las bifurcaciones lógicas, la variable podría quedar indefinida al momento de guardarse en la base de datos, provocando un colapso en tiempo de ejecución (*Runtime Error*). Filtrar por estas reglas críticas asegura la estabilidad del núcleo del software antes de preocuparnos por estándares cosméticos o de estilo (como los *docstrings* o nombres de variables).

---

## --- SECCIÓN 4: Método formal conceptual ---

### a) Describan un invariante para una clase o función importante de su sistema.
**Invariante del Stock de Producto:** > "Para cualquier producto existente en el sistema de la ferretería, el valor del campo `stock_actual` nunca puede ser un número negativo ($stock\_actual \ge 0$)."

Este invariante es una regla de negocio fundamental que debe mantenerse cierta antes y después de cualquier operación que altere el inventario (como la ejecución de la función `registrar_movimiento`). Físicamente, una ferretería no puede tener $-5$ destornilladores en sus estanterías; un stock menor a cero rompería la coherencia lógica de las alertas y de las reposiciones.

### b) Expliquen cómo lo probarían (con una prueba unitaria que verifique esa propiedad).
Para garantizar este invariante, diseñaríamos una prueba unitaria automatizada (usando el framework `pytest` o `unittest` de Python) que intente forzar una violación de la regla y verifique que el sistema responda bloqueando la operación con una excepción controlada.

**Ejemplo de implementación de la prueba en código:**

```python
import pytest
from app import registrar_movimiento, Producto, ValueError

def test_invariante_stock_no_negativo():
    # 1. Arrange: Configurar un producto con stock bajo
    producto_test = Producto(id=1, nombre="Martillo", stock_actual=3)
    
    # 2. Act & Assert: Intentar registrar una salida que supere el stock existente (3 - 5 = -2)
    # El sistema debe interceptar esto y lanzar un ValueError, impidiendo que el stock baje de 0
    with pytest.raises(ValueError) as exc_info:
        registrar_movimiento(producto_id=1, tipo="salida", cantidad=5)
    
    # 3. Assert adicional: Verificar que el stock se mantuvo intacto y seguro en su valor original
    assert producto_test.stock_actual == 3
    assert "Stock insuficiente" in str(exc_info.value)



## --- SECCIÓN 5: Reunión de validación (simulación) ---

Para la próxima **Sprint Review**, aprovechando la presencia del Product Owner (quien actúa como nexo con las necesidades reales del encargado de la ferretería), plantearemos las siguientes dos preguntas clave enfocadas puramente en la validación del negocio:

1. **Con respecto al módulo de alertas:** *“Al observar la pantalla actual de alertas por stock bajo, ¿considera que los datos de 'producto' y 'cantidad mínima a reponer' son suficientes para que el encargado tome la decisión de compra en el momento, o es indispensable visualizar también el nombre del proveedor habitual y su información de contacto en esta misma vista para agilizar el proceso?”*
   * **Objetivo:** Validar si el diseño conceptual de la alerta resuelve el problema operativo real o si carece de datos contextuales críticos para el usuario.

2. **Con respecto a la carga del archivo Excel:** *“Durante la simulación del flujo de importación, el sistema procesa el archivo del proveedor y actualiza el stock de forma automática en segundo plano. Desde la perspectiva del negocio, ¿el encargado requiere una pantalla intermedia de confirmación que le muestre un resumen de los cambios detectados antes de impactar definitivamente la base de datos, o prefiere el procesamiento directo tal como está implementado?”*
   * **Objetivo:** Validar si el flujo de interacción y los niveles de control son amigables y generan confianza en un usuario sin conocimientos técnicos profundos.
