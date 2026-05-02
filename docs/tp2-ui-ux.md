# A2. Análisis de usuario, tarea y contexto

El sistema FerreteriaStock está orientado principalmente a dos perfiles de usuario dentro de una ferretería: el empleado operativo y el encargado del local. El empleado utiliza el sistema para tareas frecuentes del día a día, como consultar productos, verificar disponibilidad, registrar entradas o salidas de mercadería y revisar el estado de determinados artículos. El encargado, además de realizar esas operaciones, necesita contar con funciones de mayor control, como dar de alta nuevos productos, supervisar alertas de stock bajo, analizar el estado general del inventario e importar archivos Excel enviados por proveedores.

Las tareas principales se concentran en mantener actualizada y confiable la información del inventario. Esto incluye buscar productos rápidamente, conocer su cantidad disponible, registrar movimientos, detectar artículos que requieren reposición y cargar datos provenientes de proveedores. Estas acciones son críticas porque impactan directamente en la atención al cliente, la organización interna del negocio y la toma de decisiones sobre compras. Un error en la carga de cantidades o una demora en encontrar un producto puede generar pérdidas de tiempo, ventas mal informadas o faltantes no detectados.

El contexto de uso corresponde a un ambiente comercial con ritmo operativo constante. Es probable que el sistema se utilice desde una computadora de escritorio o notebook ubicada en el local, mientras el usuario atiende clientes, controla mercadería o revisa pedidos. Por este motivo, la interfaz debe permitir acciones rápidas, ofrecer información clara y reducir la cantidad de pasos necesarios para completar una tarea. La prioridad no es solo que el sistema tenga muchas funciones, sino que las funciones esenciales sean fáciles de encontrar y utilizar en situaciones reales de trabajo.

También debe considerarse que no todos los usuarios tendrán conocimientos técnicos avanzados. Por eso, el diseño debe evitar pantallas sobrecargadas, mensajes ambiguos y formularios difíciles de interpretar. Los botones principales deben estar visibles, los campos deben indicar con claridad qué dato se espera ingresar y los mensajes de confirmación o error deben ayudar al usuario a entender qué ocurrió. Una interfaz adecuada para este contexto debe ser simple, consistente y confiable, especialmente porque trabaja con información sensible para el funcionamiento diario del negocio.

# A3. Auditoría de usabilidad según ISO 9241-11

La norma ISO 9241-11 plantea que la usabilidad puede analizarse a partir de tres criterios principales: eficacia, eficiencia y satisfacción. Para esta auditoría se seleccionan dos criterios especialmente relevantes para FerreteriaStock: **eficacia** y **eficiencia**.

Estos criterios permiten evaluar si el prototipo ayuda al usuario a completar correctamente las tareas principales del sistema y si puede hacerlo con una cantidad razonable de tiempo, pasos e interacción.

---

## Criterio 1: Eficacia

### Definición del criterio

La eficacia se refiere al grado en que el usuario logra completar correctamente una tarea determinada. En el caso de FerreteriaStock, este criterio es fundamental porque el sistema trabaja con información sensible para el negocio, como productos, cantidades disponibles, movimientos de mercadería y alertas de reposición.

Una interfaz eficaz debe permitir que el usuario complete tareas como buscar un producto, registrar un movimiento de stock o detectar un artículo con bajo stock sin cometer errores importantes.

---

### Métrica propuesta

**Porcentaje de usuarios que completan correctamente una tarea sin asistencia.**

La métrica se puede calcular de la siguiente manera:

```text
Eficacia = (cantidad de usuarios que completan la tarea correctamente / cantidad total de usuarios evaluados) × 100
