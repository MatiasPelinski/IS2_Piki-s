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
