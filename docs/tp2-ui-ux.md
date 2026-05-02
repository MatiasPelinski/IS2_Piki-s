# A2. Análisis de usuario, tarea y contexto

El sistema Stockeado está orientado principalmente a dos perfiles de usuario dentro de una ferretería: el empleado operativo y el encargado del local. El empleado utiliza el sistema para tareas frecuentes del día a día, como consultar productos, verificar disponibilidad, registrar entradas o salidas de mercadería y revisar el estado de determinados artículos. El encargado, además de realizar esas operaciones, necesita contar con funciones de mayor control, como dar de alta nuevos productos, supervisar alertas de stock bajo, analizar el estado general del inventario e importar archivos Excel enviados por proveedores.

Las tareas principales se concentran en mantener actualizada y confiable la información del inventario. Esto incluye buscar productos rápidamente, conocer su cantidad disponible, registrar movimientos, detectar artículos que requieren reposición y cargar datos provenientes de proveedores. Estas acciones son críticas porque impactan directamente en la atención al cliente, la organización interna del negocio y la toma de decisiones sobre compras. Un error en la carga de cantidades o una demora en encontrar un producto puede generar pérdidas de tiempo, ventas mal informadas o faltantes no detectados.

El contexto de uso corresponde a un ambiente comercial con ritmo operativo constante. Es probable que el sistema se utilice desde una computadora de escritorio o notebook ubicada en el local, mientras el usuario atiende clientes, controla mercadería o revisa pedidos. Por este motivo, la interfaz debe permitir acciones rápidas, ofrecer información clara y reducir la cantidad de pasos necesarios para completar una tarea. La prioridad no es solo que el sistema tenga muchas funciones, sino que las funciones esenciales sean fáciles de encontrar y utilizar en situaciones reales de trabajo.

También debe considerarse que no todos los usuarios tendrán conocimientos técnicos avanzados. Por eso, el diseño debe evitar pantallas sobrecargadas, mensajes ambiguos y formularios difíciles de interpretar. Los botones principales deben estar visibles, los campos deben indicar con claridad qué dato se espera ingresar y los mensajes de confirmación o error deben ayudar al usuario a entender qué ocurrió. Una interfaz adecuada para este contexto debe ser simple, consistente y confiable, especialmente porque trabaja con información sensible para el funcionamiento diario del negocio.

````markdown
# A3. Auditoría de usabilidad según ISO 9241-11

La norma ISO 9241-11 define la usabilidad como el grado en que un producto puede ser utilizado por usuarios específicos para alcanzar objetivos específicos con **eficacia**, **eficiencia** y **satisfacción** en un contexto de uso determinado.

Para el sistema **Stockeado** se seleccionan dos criterios principales de evaluación: **eficacia** y **eficiencia**. Ambos resultan adecuados para esta etapa del proyecto porque permiten analizar si el usuario puede completar correctamente las tareas principales y si puede hacerlo de manera rápida y simple dentro del contexto operativo de una ferretería.

---

## Criterio 1: Eficacia

### Definición

La eficacia se refiere a la capacidad del usuario para completar correctamente una tarea. En **Stockeado**, este criterio es fundamental porque el sistema trabaja con información crítica para el negocio: productos, cantidades disponibles, movimientos de stock y alertas de reposición.

Una interfaz eficaz debe permitir que el usuario realice tareas como buscar un producto, registrar un movimiento de stock o detectar artículos con bajo stock sin cometer errores que afecten la información del inventario.

---

### Tarea evaluada

Para evaluar este criterio se selecciona la siguiente tarea:

**Registrar una salida de stock de un producto existente.**

Esta tarea es relevante porque representa una operación frecuente dentro del sistema. Además, si se realiza de manera incorrecta, puede generar inconsistencias en el inventario, como descontar unidades de un producto equivocado o intentar retirar más cantidad de la disponible.

---

### Métrica propuesta

La métrica elegida es:

**Porcentaje de usuarios que completan correctamente la tarea sin asistencia.**

Se calcula de la siguiente manera:

```text
Eficacia = (cantidad de usuarios que completan la tarea correctamente / cantidad total de usuarios evaluados) × 100
````

---

### Simulación de evaluación en el prototipo

Para simular la evaluación, se puede pedir a 5 usuarios representativos que realicen el flujo dentro del prototipo navegable de Figma.

El flujo esperado sería:

1. Ingresar al panel principal.
2. Acceder al módulo de movimientos.
3. Seleccionar un producto existente.
4. Elegir el tipo de movimiento “Salida”.
5. Ingresar una cantidad válida.
6. Confirmar el registro.
7. Verificar que el stock se haya actualizado.

Ejemplo de resultados simulados:

| Usuario   | ¿Completó la tarea correctamente? | Observación                                                        |
| --------- | --------------------------------- | ------------------------------------------------------------------ |
| Usuario 1 | Sí                                | Completó el flujo sin inconvenientes.                              |
| Usuario 2 | Sí                                | Dudó al elegir el tipo de movimiento, pero finalizó correctamente. |
| Usuario 3 | No                                | Confundió “Salida” con “Ajuste”.                                   |
| Usuario 4 | Sí                                | Registró la salida correctamente.                                  |
| Usuario 5 | Sí                                | Completó el flujo correctamente.                                   |

Resultado simulado:

```text
Eficacia = (4 / 5) × 100 = 80%
```

---

### Análisis del resultado

El resultado simulado indica que la mayoría de los usuarios podría completar la tarea, pero también muestra un posible problema de interpretación en el formulario de movimientos. La confusión entre “Salida” y “Ajuste” puede provocar errores importantes, ya que ambos conceptos modifican el stock de manera diferente.

Una salida descuenta unidades del inventario, mientras que un ajuste reemplaza el valor actual por una nueva cantidad. Si el usuario no comprende esta diferencia, podría modificar incorrectamente el stock de un producto.

---

### Mejora propuesta

Para mejorar la eficacia del formulario, se propone agregar una descripción breve debajo del campo “Tipo de movimiento”:

```text
Entrada: aumenta el stock del producto.
Salida: disminuye el stock del producto.
Ajuste: reemplaza el stock actual por una cantidad exacta.
```

También se recomienda incorporar una confirmación previa antes de guardar el movimiento, especialmente en operaciones de salida o ajuste. Esta confirmación debería mostrar:

```text
Producto seleccionado
Stock actual
Tipo de movimiento
Cantidad ingresada
Stock resultante
```

De esta manera, el usuario puede revisar la operación antes de confirmarla y se reduce la posibilidad de errores en la carga de datos.

---

## Criterio 2: Eficiencia

### Definición

La eficiencia mide los recursos que necesita el usuario para completar una tarea. En una interfaz, puede medirse mediante el tiempo utilizado, la cantidad de clics o la cantidad de pasos necesarios para alcanzar un objetivo.

En **Stockeado**, la eficiencia es especialmente importante porque el sistema será utilizado en un contexto operativo. El usuario puede necesitar consultar productos o registrar movimientos mientras atiende clientes, revisa mercadería o controla pedidos. Por lo tanto, las tareas frecuentes deben poder realizarse de manera rápida y con pocos pasos.

---

### Tarea evaluada

Para evaluar este criterio se selecciona la siguiente tarea:

**Buscar un producto específico en el inventario y verificar su stock actual.**

Esta tarea fue elegida porque representa una de las acciones más habituales dentro de una ferretería. Ante la consulta de un cliente o al revisar mercadería, el usuario necesita saber rápidamente si un producto está disponible y cuántas unidades quedan.

---

### Métrica propuesta

La métrica principal es:

**Tiempo promedio necesario para encontrar un producto y consultar su stock actual.**

Se calcula de la siguiente manera:

```text
Tiempo promedio = suma de los tiempos individuales / cantidad total de usuarios evaluados
```

Como métrica complementaria, también puede medirse:

```text
Cantidad promedio de clics necesarios para completar la tarea
```

---

### Simulación de evaluación en el prototipo

Para simular la evaluación, se puede pedir a 5 usuarios que busquen un producto específico, por ejemplo “Martillo 500g”, desde el dashboard o desde la pantalla de inventario.

Ejemplo de resultados simulados:

| Usuario   | Tiempo utilizado | Cantidad de clics | Resultado                                               |
| --------- | ---------------- | ----------------- | ------------------------------------------------------- |
| Usuario 1 | 18 segundos      | 3 clics           | Encontró el producto.                                   |
| Usuario 2 | 22 segundos      | 4 clics           | Encontró el producto.                                   |
| Usuario 3 | 30 segundos      | 5 clics           | Tardó más porque no identificó rápidamente el buscador. |
| Usuario 4 | 19 segundos      | 3 clics           | Encontró el producto.                                   |
| Usuario 5 | 21 segundos      | 4 clics           | Encontró el producto.                                   |

Resultado simulado:

```text
Tiempo promedio = (18 + 22 + 30 + 19 + 21) / 5 = 22 segundos
```

---

### Análisis del resultado

El resultado simulado muestra que la tarea puede completarse, pero también evidencia que la eficiencia depende mucho de la visibilidad del buscador y de la organización de la pantalla. Si el usuario no identifica rápidamente dónde buscar, aumenta el tiempo necesario para consultar un producto.

En una ferretería con muchos artículos cargados, recorrer manualmente una tabla completa no sería práctico. Por eso, el buscador y los filtros deben ser elementos centrales de la interfaz, no funciones secundarias o poco visibles.

---

### Mejora propuesta

Para mejorar la eficiencia, se propone mantener siempre visible un buscador por nombre o descripción del producto dentro del módulo de inventario. Además, debería incluirse un filtro por categoría para reducir la cantidad de resultados cuando el inventario sea amplio.

También se recomienda incorporar accesos rápidos desde el dashboard a las tareas más frecuentes:

```text
Buscar producto
Registrar movimiento
Ver productos con stock bajo
Importar Excel de proveedor
```

Otra mejora importante es destacar visualmente los productos con stock bajo mediante etiquetas o colores consistentes. Esto permite que el usuario identifique situaciones críticas sin tener que revisar manualmente cada fila de la tabla.

---

# Relación con el ciclo de diseño centrado en el usuario según ISO 13407

La ISO 13407 propone un proceso de diseño centrado en el usuario, basado en comprender el contexto de uso, identificar las necesidades de los usuarios, diseñar soluciones y evaluarlas de manera iterativa.

El proceso seguido en **Stockeado** se alinea con este enfoque porque parte del análisis de los usuarios reales del sistema: empleados y encargados de una ferretería. A partir de esos perfiles, se identifican sus tareas principales, como consultar productos, registrar movimientos, controlar alertas e importar información de proveedores.

Luego, esas necesidades se trasladan a un prototipo navegable en Figma, compuesto por pantallas que representan el flujo principal del sistema. Esto permite visualizar la experiencia antes de avanzar completamente con la implementación, reduciendo el riesgo de construir una interfaz poco clara o difícil de usar.

La evaluación mediante criterios de usabilidad permite detectar problemas concretos. Por ejemplo, si un usuario tarda demasiado en encontrar un producto, el diseño puede mejorarse haciendo más visible el buscador. Si un usuario confunde los tipos de movimiento, se pueden agregar descripciones o confirmaciones antes de guardar la operación.

De esta manera, el diseño no se plantea como una decisión cerrada, sino como un proceso iterativo. Se analiza el contexto, se diseña una solución, se evalúa su uso y se proponen mejoras. Esto permite que el sistema evolucione en función de las necesidades reales de los usuarios y no únicamente desde una perspectiva técnica.

---

# Conclusión de la auditoría

La auditoría de usabilidad permite identificar aspectos positivos y puntos de mejora en el prototipo actual de **Stockeado**. Desde el criterio de eficacia, el sistema debe asegurar que los usuarios puedan completar tareas críticas sin cometer errores que afecten el inventario. Desde el criterio de eficiencia, la interfaz debe permitir realizar consultas y operaciones frecuentes de manera rápida y con pocos pasos.

Las mejoras propuestas se enfocan en reducir errores, aclarar conceptos importantes y facilitar el acceso a las funciones más utilizadas. Esto contribuye a que el sistema sea más adecuado para el contexto real de una ferretería, donde la rapidez, la claridad y la confiabilidad de la información son fundamentales.

```
```
