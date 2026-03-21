
![Matriz 2](https://github.com/user-attachments/assets/af14905f-4f83-4baa-ba72-f40a8d590ee1)

# PLAN DE CONTINGENCIA

## Sistema de Gestión de Inventario – Ferretería

El presente plan tiene como objetivo definir, para cada riesgo identificado, dos aspectos fundamentales:

* **Estrategias de mitigación**: acciones preventivas orientadas a reducir la probabilidad de ocurrencia del riesgo.
* **Plan de contingencia**: acciones correctivas que se ejecutarán en caso de que el riesgo se materialice, con el fin de minimizar su impacto en el sistema y en la operación del negocio.

Se priorizan especialmente los riesgos que afectan la **consistencia del stock**, dado que este constituye el núcleo funcional del sistema.

---

## Riesgo 1

**Registro incorrecto de entradas y salidas de stock por parte de los empleados**

### Estrategia de mitigación

Para reducir la probabilidad de errores humanos en la carga de datos, se implementarán múltiples mecanismos de control en distintos niveles del sistema:

* Validaciones tanto en frontend como en backend que verifiquen:

  * Tipos de datos correctos.
  * Rangos válidos (por ejemplo, evitar cantidades negativas).
  * Coherencia lógica (no permitir salidas superiores al stock disponible).
* Diseño de interfaz de usuario (UX) orientado a minimizar errores, mediante:

  * Formularios claros.
  * Uso de campos estructurados.
  * Confirmaciones antes de registrar movimientos críticos.
* Capacitación básica a los usuarios finales (empleados), enfocada en el uso correcto del sistema.
* Implementación de restricciones de negocio en la lógica del sistema para evitar estados inválidos.

### Plan de contingencia

En caso de detectarse inconsistencias en el stock:

* Se utilizará un **registro histórico de movimientos (log de auditoría)** que almacene:

  * Fecha y hora.
  * Usuario responsable.
  * Tipo de operación (entrada/salida).
  * Motivo.
* Se habilitará la **corrección manual controlada**, accesible únicamente a usuarios con permisos elevados (por ejemplo, encargado).
* Se generarán **reportes de inconsistencias** que permitan identificar rápidamente desvíos en el inventario.
* En situaciones críticas, se procederá a la **reconstrucción del stock** a partir del historial de movimientos registrados.

---

## Riesgo 2

**Definición inadecuada del stock mínimo por producto**

### Estrategia de mitigación

Dado que el stock mínimo es un parámetro clave para la generación de alertas y reposición:

* Se realizará un relevamiento inicial con el cliente para definir valores adecuados por tipo de producto.
* Se establecerán valores por defecto basados en categorías, permitiendo una configuración inicial coherente.
* Se implementarán validaciones que eviten configuraciones extremas o incoherentes.
* Se documentarán criterios de definición de stock mínimo para facilitar su mantenimiento.

### Plan de contingencia

En caso de detectar configuraciones incorrectas:

* Se permitirá la **modificación dinámica del stock mínimo** sin necesidad de interrumpir el sistema.
* Se generarán **alertas manuales temporales** mientras se corrigen los valores.
* Se implementará un listado de productos con comportamiento anómalo (por ejemplo, alertas constantes o ausencia de alertas).
* Se realizará una revisión periódica de productos críticos junto al responsable del negocio.

---

## Riesgo 3

**Problemas de concurrencia en operaciones de stock**

### Estrategia de mitigación

Dado que múltiples usuarios pueden operar simultáneamente:

* Se implementarán **transacciones en base de datos** para garantizar la atomicidad de las operaciones.
* Se utilizarán mecanismos de **bloqueo (locking)** para evitar modificaciones simultáneas conflictivas.
* Se diseñará la lógica de actualización de stock de forma que sea **consistente y segura frente a concurrencia**.
* Se validará el estado del stock antes y después de cada operación.

### Plan de contingencia

Si se detectan inconsistencias derivadas de concurrencia:

* Se analizarán los registros de operaciones con marca temporal (timestamp) para identificar el origen del conflicto.
* Se ejecutarán procesos de **reconciliación de datos**, recalculando el stock en base al historial.
* Se podrá restringir temporalmente la ejecución de ciertas operaciones hasta resolver la inconsistencia.
* Se aplicarán mecanismos de control adicionales en puntos críticos del sistema.

---

## Riesgo 4

**Falta de trazabilidad en los movimientos de stock**

### Estrategia de mitigación

Para garantizar la auditabilidad del sistema:

* Se diseñará desde el inicio un **modelo de auditoría completo**, donde cada movimiento registre:

  * Usuario.
  * Fecha.
  * Tipo de operación.
  * Motivo.
* Se hará obligatorio el registro del motivo en cada operación.
* Se integrará la trazabilidad como parte del modelo de datos, no como una funcionalidad opcional.

### Plan de contingencia

En caso de ausencia o insuficiencia de trazabilidad:

* Se implementará un sistema de logging a partir del momento de detección.
* Se restringirán operaciones críticas hasta garantizar un nivel mínimo de trazabilidad.
* Se realizará una auditoría manual para reconstruir eventos relevantes en la medida de lo posible.
* Se marcarán registros como “no confiables” cuando no sea posible garantizar su integridad.

---

## Riesgo 5

**Errores derivados del ingreso manual de datos sin validaciones adecuadas**

### Estrategia de mitigación

Para reducir errores en datos maestros (productos):

* Se implementarán validaciones estrictas en:

  * Precio (valores positivos, rangos razonables).
  * Cantidades.
  * Categorías (listas predefinidas).
* Se utilizarán controles de interfaz como:

  * Listas desplegables.
  * Autocompletado.
  * Campos obligatorios.
* Se centralizará la lógica de validación en el backend para asegurar consistencia.

### Plan de contingencia

Ante la detección de datos incorrectos:

* Se habilitará un módulo de **edición controlada de productos**.
* Se generarán reportes de datos atípicos o inconsistentes.
* Se permitirá revertir cambios recientes mediante mecanismos de rollback.
* Se realizará una revisión periódica de los datos críticos del sistema.

---

# Conclusión

El plan de contingencia propuesto permite abordar de manera estructurada los principales riesgos del sistema de gestión de inventario, combinando medidas preventivas y correctivas.

Se destaca que:

* Los riesgos fueron definidos en función del dominio específico del sistema.
* Las estrategias propuestas contemplan tanto aspectos técnicos como operativos.
* Se prioriza la integridad y confiabilidad del stock como eje central del sistema.

Este enfoque no solo mejora la calidad del producto final, sino que también demuestra una correcta aplicación de los principios de **gestión de riesgos en Ingeniería de Software**. 

![Matriz 1](https://github.com/user-attachments/assets/29fe6a72-4861-4a34-a5bb-bcef7e23b8b2)

# PLAN DE CONTINGENCIA

## Sistema de Gestión de Inventario – Versión General del Proyecto

El presente plan de contingencia se desarrolla a partir de los riesgos identificados en la matriz inicial del proyecto. Se contemplan tanto **estrategias de mitigación (preventivas)** como **acciones de contingencia (correctivas)**, con el objetivo de asegurar la continuidad del desarrollo y minimizar impactos negativos en el sistema.

Se incluyen riesgos técnicos, organizacionales, de requisitos y externos, cubriendo así las principales dimensiones del proyecto.

---

## Riesgo 1

**El equipo no tiene experiencia con el framework web elegido**

### Estrategia de mitigación

Dado que este riesgo impacta directamente en la productividad inicial del equipo:

* Se realizará una **fase de capacitación inicial**, donde los integrantes se familiaricen con el framework seleccionado.
* Se desarrollarán **prototipos o pruebas de concepto (POC)** para validar el uso de la tecnología antes de avanzar en funcionalidades complejas.
* Se promoverá el uso de **documentación oficial, tutoriales y recursos técnicos confiables**.
* Se dividirán las tareas de manera que los integrantes con mayor conocimiento puedan asistir a los menos experimentados.
* Se adoptarán buenas prácticas de desarrollo incremental para reducir la complejidad inicial.

### Plan de contingencia

En caso de que la falta de experiencia genere retrasos significativos:

* Se evaluará la **simplificación del alcance técnico** en las primeras iteraciones.
* Se reasignarán tareas críticas a los integrantes con mayor dominio tecnológico.
* Se considerará el uso de **plantillas, librerías o soluciones preexistentes** para acelerar el desarrollo.
* En situaciones extremas, se analizará la **posibilidad de migrar a una tecnología más conocida**, evaluando el costo-beneficio.

---

## Riesgo 2

**Cambios en los requerimientos del cliente**

### Estrategia de mitigación

Dado que este riesgo es inherente a metodologías ágiles:

* Se establecerá un **backlog claramente definido y priorizado**.
* Se documentarán los requerimientos de forma detallada desde el inicio.
* Se implementará un proceso de **gestión de cambios (Change Request)**.
* Se realizarán revisiones periódicas con el cliente para validar avances.
* Se utilizará un tablero Kanban para visualizar el estado de las tareas.

### Plan de contingencia

En caso de cambios no previstos:

* Se evaluará el impacto del cambio en términos de tiempo y complejidad.
* Se replanificará el backlog priorizando funcionalidades críticas.
* Se pospondrán funcionalidades secundarias si es necesario.
* Se documentarán todos los cambios para mantener trazabilidad.
* Se comunicará al equipo el nuevo alcance para evitar inconsistencias.

---

## Riesgo 3

**Falta de coordinación entre los integrantes del equipo**

### Estrategia de mitigación

Para evitar problemas organizacionales:

* Se definirán roles claros (Scrum Master, Dev Lead, QA, UX).
* Se establecerán **reuniones periódicas de seguimiento** (stand-ups).
* Se utilizarán herramientas colaborativas (GitHub, Kanban).
* Se definirán estándares de trabajo (nomenclatura, commits, ramas).
* Se fomentará la comunicación constante entre integrantes.

### Plan de contingencia

Si se detectan problemas de coordinación:

* Se realizará una **reorganización de tareas**.
* Se redefinirán responsabilidades individuales.
* Se establecerán reuniones adicionales de alineación.
* Se revisará el estado del proyecto para detectar inconsistencias.
* El Scrum Master intervendrá para corregir desviaciones en el proceso.

---

## Riesgo 4

**Errores en el manejo del stock**

### Estrategia de mitigación

Dado que el stock es el núcleo del sistema:

* Se implementarán **validaciones estrictas** en todas las operaciones.
* Se diseñará una lógica de negocio robusta que evite estados inválidos.
* Se desarrollarán **pruebas unitarias** para verificar el correcto funcionamiento.
* Se registrarán todas las operaciones de stock.
* Se definirá claramente el flujo de entradas y salidas.

### Plan de contingencia

En caso de inconsistencias en el stock:

* Se utilizará el historial de operaciones para detectar errores.
* Se permitirá la corrección manual bajo control de permisos.
* Se recalculará el stock en base a los movimientos registrados.
* Se generarán reportes de inconsistencias.
* Se bloquearán temporalmente operaciones críticas si es necesario.

---

## Riesgo 5

**Problemas con acceso a internet o herramientas**

### Estrategia de mitigación

Para reducir dependencia de factores externos:

* Se utilizarán herramientas confiables (GitHub, Figma).
* Se realizarán commits frecuentes para evitar pérdida de trabajo.
* Se mantendrán copias locales del proyecto.
* Se planificarán tareas offline cuando sea posible.
* Se verificará la conectividad antes de reuniones importantes.

### Plan de contingencia

Ante fallas externas:

* Se continuará el desarrollo en entorno local.
* Se sincronizarán cambios cuando se restablezca la conexión.
* Se reprogramarán reuniones afectadas.
* Se utilizarán canales alternativos de comunicación.
* Se priorizarán tareas que no dependan de conexión externa.

---

# Conclusión

El presente plan de contingencia permite gestionar de manera integral los riesgos identificados en la matriz inicial del proyecto, abordando tanto aspectos técnicos como organizacionales y externos.

Se destacan los siguientes puntos:

* Se definieron estrategias preventivas orientadas a reducir la probabilidad de ocurrencia de los riesgos.
* Se establecieron planes de acción concretos para responder ante la materialización de cada riesgo.
* Se consideraron tanto el desarrollo del sistema como la dinámica del equipo de trabajo.

Este enfoque demuestra una correcta aplicación de los principios de **gestión de riesgos en Ingeniería de Software**, permitiendo mejorar la previsibilidad del proyecto y garantizar una mayor calidad en el producto final.
