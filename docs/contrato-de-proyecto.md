# CONTRATO DE PROYECTO

## Sistema de Gestión de Inventario para Ferretería — "Stockeado"

---

### 1. Identificación del Proyecto

| Campo | Valor |
|-------|-------|
| **Nombre del proyecto** | Stockeado |
| **Nombre del grupo** | Piki's |
| **Materia** | Ingeniería de Software II |
| **Institución** | Universidad de la Cuenca del Plata (UCP) |
| **Año académico** | 2026 |

---

### 2. Integrantes del equipo y roles

| Nombre | Rol | Responsabilidad principal |
|--------|-----|---------------------------|
| Victoria Espinola | Scrum Master | Facilitar el proceso ágil, eliminar impedimentos, garantizar que el equipo siga la metodología. |
| Matías Pelinski | QA Lead | Definir y ejecutar pruebas de calidad, garantizar que el sistema cumpla con los requisitos. |
| Lisandro Mieres | Dev Lead | Liderar el desarrollo técnico, revisar código, asegurar buenas prácticas de programación. |
| Emilia Auras | UX Lead | Diseñar la experiencia de usuario, garantizar usabilidad y accesibilidad del sistema. |

---

### 3. Descripción del proyecto

**Propósito:**
Desarrollar un sistema de gestión de inventario para una ferretería mediana, capaz de llevar un seguimiento preciso del stock de productos y generar alertas automáticas cuando un producto esté por debajo de una cantidad mínima establecida, permitiendo solicitar reposición de manera oportuna.

**Alcance funcional:**

El sistema incluirá las siguientes funcionalidades:

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| F01 | Autenticación de usuarios | Login con email y contraseña, diferenciando roles (Encargado y Empleado). |
| F02 | Gestión de productos | ABM (alta, baja, modificación) de productos, con campos: nombre, descripción, precio, stock actual, stock mínimo, categoría, proveedor. |
| F03 | Control de stock | Registro de movimientos de inventario (entradas, salidas, ajustes) con fecha, cantidad, motivo y usuario responsable. |
| F04 | Alertas automáticas | Generación de alertas cuando el stock actual sea menor al stock mínimo. |
| F05 | Listado de reposición | Visualización de productos que necesitan reposición, con cantidad sugerida. |
| F06 | Importación de Excel | Carga masiva de productos desde archivos Excel enviados por proveedores, con opción de vincular productos nuevos a existentes. |
| F07 | Dashboard | Panel de control con estadísticas: total de productos, alertas activas, productos a reponer, movimientos del día. |
| F08 | Historial de movimientos | Registro completo de todas las operaciones de stock con trazabilidad. |
| F09 | Búsqueda y filtros | Búsqueda de productos por nombre y filtro por categoría. |

**Alcance técnico:**

| Componente | Tecnología |
|------------|------------|
| Backend | Python con Flask |
| Frontend | HTML, CSS, JavaScript (Jinja2 templates) |
| Base de datos | MySQL (XAMPP) |
| Librerías adicionales | mysql-connector-python, openpyxl, Feather Icons |
| Control de versiones | Git + GitHub |
| Metodología | Scrum / Kanban |

**Fuera de alcance:**

- Desarrollo de aplicación móvil nativa (solo web)
- Integración con sistemas de facturación externos
- Módulo de ventas al contado (solo control de stock)
- Envío automático de emails o notificaciones push
- Módulo de gestión de usuarios avanzada (recuperación de contraseña, etc.)

---

### 4. Entregables del proyecto

| Entregable | Fecha estimada | Formato |
|------------|----------------|---------|
| TP1 — Diseño y planificación | Semana 4 | Documento PDF + Repositorio GitHub |
| TP2 — Desarrollo de funcionalidades core | Semana 8 | Sistema funcionando + Documentación técnica |
| TP3 — Sistema completo e integración | Semana 12 | Sistema completo + Manual de usuario |
| Presentación final | Semana 13/14 | Presentación oral + Demo en vivo |

**Artefactos específicos por TP:**

**TP1:**
- Diagrama de clases (proto-clases)
- Matriz de riesgos
- Tablero Kanban en GitHub Projects
- Estructura de base de datos (script SQL)
- Login funcional

**TP2:**
- Todos los casos de uso implementados
- Patrones de diseño aplicados (Observer, Strategy)
- Dashboard con estadísticas
- Módulo de movimientos de stock
- Alertas automáticas

**TP3:**
- Sistema completo funcionando
- Importación de Excel con gestión de productos nuevos
- Tema claro/oscuro
- Documentación completa
- Manual de usuario

---

### 5. Cronograma de hitos

| Hito | Semana | Descripción |
|------|--------|-------------|
| Kick-off | Semana 1 | Definición del proyecto, asignación de roles |
| Diseño de base de datos | Semana 2 | Esquema MySQL, relaciones, script SQL |
| Prototipo de login | Semana 3 | Autenticación funcional |
| TP1 - Entrega | Semana 4 | Diseño y planificación |
| Desarrollo core | Semanas 5-7 | Productos, movimientos, alertas |
| TP2 - Entrega | Semana 8 | Funcionalidades core |
| Mejoras e integración | Semanas 9-11 | Importación Excel, UI/UX, pruebas |
| TP3 - Entrega | Semana 12 | Sistema completo |
| Presentación final | Semana 13-14 | Demo y defensa |

---

### 6. Metodología de trabajo

**Framework ágil:** Scrum adaptado con tablero Kanban en GitHub Projects.

**Ceremonias:**

| Ceremonia | Frecuencia | Duración | Participantes |
|-----------|------------|----------|---------------|
| Daily meeting | Diaria (asincrónica vía chat) | 15 min | Todo el equipo |
| Sprint planning | Cada 2 semanas | 60 min | Todo el equipo |
| Sprint review | Cada 2 semanas | 45 min | Todo el equipo |
| Sprint retrospective | Cada 2 semanas | 30 min | Todo el equipo |

**Herramientas de colaboración:**

| Herramienta | Uso |
|-------------|-----|
| GitHub | Repositorio de código, control de versiones |
| GitHub Projects | Tablero Kanban, seguimiento de tareas |
| Discord / WhatsApp | Comunicación diaria |
| VS Code Live Share | Programación colaborativa |

**Definición de "Done" (terminado):**

Una tarea se considera terminada cuando:
1. El código está escrito y funciona localmente
2. Las pruebas básicas pasan (sin errores evidentes)
3. El código está subido a GitHub (branch correspondiente)
4. La tarea está movida a "Done" en el Kanban
5. El responsable de QA lo ha revisado (cuando corresponda)

---

### 7. Roles y responsabilidades detalladas

**Scrum Master — Victoria Espinola**
- Facilitar las ceremonias ágiles
- Eliminar impedimentos del equipo
- Actualizar y mantener el tablero Kanban
- Gestionar la comunicación con el profesor
- Asegurar que el equipo siga la metodología

**QA Lead — Matías Pelinski**
- Definir casos de prueba
- Ejecutar pruebas de regresión
- Documentar bugs y errores
- Verificar que los criterios de aceptación se cumplan
- Aprobar releases antes de la entrega

**Dev Lead — Lisandro Mieres**
- Liderar el desarrollo técnico
- Revisar el código del equipo (code reviews)
- Mantener la calidad y consistencia del código
- Resolver problemas técnicos complejos
- Asegurar la integración de componentes

**UX Lead — Emilia Auras**
- Diseñar la interfaz de usuario
- Garantizar la usabilidad del sistema
- Crear prototipos (si aplica)
- Validar que la experiencia de usuario sea intuitiva
- Documentar decisiones de diseño

---

### 8. Riesgos identificados y mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|-------------|
| Falta de experiencia técnica con Flask | Alta | Medio | Capacitación interna, documentación oficial, consulta con IA |
| Problemas de integración con MySQL | Media | Alto | Pruebas tempranas de conexión, uso de XAMPP estandarizado |
| Conflictos de horarios entre integrantes | Alta | Medio | Trabajo asincrónico, reuniones planificadas, uso de GitHub |
| Cambios en requisitos durante el desarrollo | Media | Medio | Sprint cortos, reuniones frecuentes con el profesor |
| Pérdida de código o datos | Baja | Alto | Commits frecuentes a GitHub, respaldos locales |
| Dependencia de IA para generación de código | Media | Bajo | Revisión manual de todo el código, documentación en AI_LOG.md |

---

### 9. Criterios de aceptación del proyecto

El proyecto se considerará aceptado cuando:

1. **Todas las funcionalidades obligatorias** (F01 a F08) estén implementadas y funcionando
2. **El sistema pase las pruebas** definidas por QA Lead
3. **No haya bugs críticos** (que impidan el uso normal del sistema)
4. **El código esté en GitHub** con commits regulares de todos los integrantes
5. **La documentación esté completa** (incluyendo AI_LOG.md)
6. **El sistema sea presentable** ante el profesor y los compañeros

---

### 10. Firma de conformidad

Al firmar este contrato, los integrantes del equipo acuerdan:

- Cumplir con los roles y responsabilidades asignados
- Respetar el cronograma de hitos y entregas
- Comunicar cualquier impedimento de manera temprana
- Colaborar activamente en el desarrollo del proyecto
- Documentar el uso de herramientas de IA en AI_LOG.md

---

| Nombre | Rol | Firma | Fecha |
|--------|-----|-------|-------|
| Victoria Espinola | Scrum Master | _________________ | ____/____/2026 |
| Matías Pelinski | QA Lead | _________________ | ____/____/2026 |
| Lisandro Mieres | Dev Lead | _________________ | ____/____/2026 |
| Emilia Auras | UX Lead | _________________ | ____/____/2026 |

---

**Fecha de vigencia:** ____/____/2026  
**Próxima revisión:** ____/____/2026 (siguiente sprint)

---

