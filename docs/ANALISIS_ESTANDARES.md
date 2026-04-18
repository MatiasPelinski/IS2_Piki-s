# Análisis de Estándares — Sistema de Gestión de Inventario

**INGENIERÍA DE SOFTWARE II · UCP · 2026**

Grupo: Auras, Espínola, Mieres, Pelinski · Proyecto: Stockeado

Eje 3 — HCI y Sistemas Críticos

---

## 1. Investigación de Estándares

### 1.1. ISO 9241-11 — Usabilidad

La norma ISO 9241-11, publicada originalmente en 1998 y revisada en 2018, establece el marco conceptual y operativo para la evaluación de la usabilidad de sistemas interactivos. Define la usabilidad como el grado en que un producto puede ser utilizado por usuarios específicos para alcanzar objetivos concretos con eficacia, eficiencia y satisfacción, en un contexto de uso determinado.

Sus tres dimensiones principales son:

- **Eficacia:** capacidad del usuario de completar una tarea y alcanzar el resultado esperado con exactitud. Se mide en términos de tasa de éxito de tareas y número de errores cometidos.
- **Eficiencia:** relación entre el resultado obtenido y los recursos consumidos para alcanzarlo (tiempo, esfuerzo cognitivo, número de pasos). Un sistema eficiente permite completar tareas con el menor costo operativo posible.
- **Satisfacción:** grado de comodidad y aceptación del usuario al interactuar con el sistema. Abarca tanto aspectos funcionales como emocionales de la experiencia de uso.

La norma subraya que la usabilidad no es una propiedad intrínseca del sistema, sino que depende del contexto de uso: el perfil del usuario, las tareas que realiza y el entorno físico y organizacional en que opera. Esta contextualización es fundamental para el diseño y la evaluación de sistemas en entornos reales.

---

### 1.2. ISO 13407 — Diseño Centrado en el Humano

La norma ISO 13407, publicada en 1999 y posteriormente reemplazada por ISO 9241-210 en 2010, establece el proceso de Diseño Centrado en el Humano (Human-Centred Design, HCD) para el desarrollo de sistemas interactivos. Su objetivo central es asegurar que las necesidades, capacidades y limitaciones de los usuarios sean incorporadas de manera sistemática en cada etapa del desarrollo.

El proceso se articula en cuatro etapas iterativas:

- **Comprender y especificar el contexto de uso:** identificar quiénes son los usuarios, qué tareas realizan, bajo qué condiciones operan el sistema y qué restricciones físicas, organizacionales o técnicas existen.
- **Especificar los requisitos del usuario y de la organización:** definir, a partir del análisis del contexto, qué necesita el sistema proporcionar para satisfacer las necesidades reales de los usuarios, evitando partir de suposiciones no validadas.
- **Producir soluciones de diseño:** generar propuestas de diseño (prototipos, maquetas, flujos de interacción) que den respuesta a los requisitos identificados, pasando de conceptos abstractos a representaciones concretas evaluables.
- **Evaluar los diseños con respecto a los requisitos:** validar las soluciones con usuarios reales en condiciones representativas del uso real. Los hallazgos de esta evaluación retroalimentan las etapas anteriores en un ciclo iterativo.

La norma establece que estas etapas deben repetirse hasta que los criterios de usabilidad y los requisitos del usuario sean satisfechos, enfatizando que la participación activa de los usuarios no es opcional sino constitutiva del proceso.

---

### 1.3. ISO/IEC 27001 — Seguridad de la Información

La norma ISO/IEC 27001, publicada en 2005 y revisada en 2013 y 2022, especifica los requisitos para establecer, implementar, mantener y mejorar continuamente un Sistema de Gestión de Seguridad de la Información (SGSI). Su objetivo es proteger los activos de información de una organización frente a amenazas internas y externas, garantizando tres propiedades fundamentales:

- **Confidencialidad:** la información solo es accesible para las personas autorizadas. Implica control de acceso, gestión de credenciales, cifrado de datos sensibles y clasificación de la información.
- **Integridad:** la información es exacta, completa y no ha sido alterada de manera no autorizada. Requiere mecanismos de validación, control de cambios, logs de auditoría y hash de integridad.
- **Disponibilidad:** la información y los sistemas que la procesan están accesibles cuando los usuarios autorizados los necesitan. Implica redundancia, planes de continuidad del negocio y gestión de incidentes.

La norma adopta un enfoque basado en riesgos: la organización debe identificar los activos de información, evaluar las amenazas y vulnerabilidades que los afectan, estimar el impacto potencial y seleccionar controles proporcionales al nivel de riesgo aceptable. Incluye un Anexo A con 93 controles organizados en cuatro dominios: organizacional, personal, físico y tecnológico.

---

### 1.4. ISA/IEC 62443 — Ciberseguridad en Sistemas de Control Industrial

La serie de normas ISA/IEC 62443, desarrollada conjuntamente por la International Society of Automation (ISA) y la IEC a partir de 2007, define los requisitos de ciberseguridad para los Sistemas de Automatización y Control Industrial (IACS). Su ámbito de aplicación cubre sistemas SCADA, controladores lógicos programables (PLC), interfaces hombre-máquina (HMI), redes de planta y cualquier componente que forme parte de la infraestructura de control de procesos físicos.

La serie se estructura en cuatro grupos de normas:

- **Serie 1 (General):** terminología, conceptos y modelos de referencia de seguridad industrial.
- **Serie 2 (Políticas y procedimientos):** gestión del programa de seguridad para operadores de sistemas de control.
- **Serie 3 (Requisitos del sistema):** requisitos de seguridad para el sistema IACS completo, incluyendo el modelo de zonas y conductos y los niveles de seguridad (Security Levels 1–4).
- **Serie 4 (Requisitos de componentes):** requisitos de seguridad aplicables a productos y componentes individuales de los fabricantes.

Una característica distintiva de este estándar es la segmentación de la red en zonas de seguridad con distintos niveles de confianza, y la definición de conductos controlados para la comunicación entre zonas. Su aplicación es obligatoria en sectores como energía, petroquímica, tratamiento de agua, manufactura crítica y transporte automatizado.

---

### 1.5. ISO 9001 — Gestión de la Calidad

La norma ISO 9001, publicada originalmente en 1987 y revisada en 2015 en su versión vigente, establece los requisitos para un Sistema de Gestión de la Calidad (SGC). A diferencia de las normas técnicas sectoriales, ISO 9001 es de aplicación transversal: define principios y procesos aplicables a cualquier organización, independientemente de su tamaño, sector o tipo de producto o servicio.

Los principios fundamentales de la norma incluyen:

- **Enfoque en el cliente:** las decisiones de diseño y proceso deben orientarse a satisfacer los requisitos explícitos e implícitos del cliente.
- **Liderazgo y compromiso:** la alta dirección debe establecer objetivos de calidad y asegurar los recursos para alcanzarlos.
- **Enfoque basado en procesos:** identificar, gestionar y optimizar los procesos interrelacionados que conforman el sistema.
- **Mejora continua:** ciclo PDCA (Planificar, Hacer, Verificar, Actuar) como motor permanente de optimización del sistema.
- **Toma de decisiones basada en evidencia:** las decisiones deben fundamentarse en el análisis de datos y hechos verificables.

En el contexto del desarrollo de software, ISO 9001 proporciona el marco para la gestión de la calidad del proceso de desarrollo: planificación de sprints, verificación de entregables, gestión de no conformidades y mejora iterativa, todos alineados con el ciclo PDCA.

---

## 2. Análisis Aplicado al Proyecto

### 2.1. Estándares más relevantes para el escenario elegido

El sistema **Stockeado** es un sistema de gestión de inventario para una ferretería mediana. Sus usuarios primarios son empleados encargados de registrar movimientos de stock y un encargado de compras con capacidad de gestión ampliada. A partir de este escenario, los estándares de mayor relevancia son:

**ISO 9241-11** es el estándar más directamente aplicable. El sistema es operado en un entorno de trabajo real, por usuarios que no necesariamente poseen formación técnica, en condiciones de alta frecuencia de uso (múltiples registros de movimientos por día). En este contexto, la eficacia de la interfaz —que el empleado complete correctamente el registro de una entrada o salida sin ambigüedades— y la eficiencia —que lo haga en el menor tiempo posible sin pasos innecesarios— son factores críticos que determinan directamente la calidad de los datos almacenados. Un error de usabilidad en la carga de stock tiene el mismo impacto operacional que un error de código: genera inconsistencias en el inventario.

**ISO 9001** resulta igualmente relevante como marco de proceso. El núcleo funcional del sistema es la calidad del proceso de control de inventario: cada movimiento debe ser correcto, completo, trazable y auditable. El historial de movimientos con usuario, fecha y motivo, el control de roles y la restricción de operaciones críticas al rol de encargado son implementaciones directas del principio de trazabilidad y responsabilidad por proceso que exige esta norma. El propio ciclo de desarrollo iterativo (Sprint 0 → TP1 → TP2) refleja el ciclo PDCA.

**ISO/IEC 27001** aplica de manera parcial pero con urgencia respecto de sus brechas actuales. El sistema gestiona credenciales de acceso, datos de stock con valor comercial y relaciones con proveedores. En su estado actual presenta no conformidades críticas —especialmente el almacenamiento de contraseñas en texto plano— que deben resolverse antes de cualquier despliegue en un entorno de producción real.

---

### 2.2. Si el sistema fuera declarado "crítico"

Para analizar este escenario, se considera una extensión realista del dominio: una ferretería industrial que comercializa materiales peligrosos (inflamables, corrosivos, productos con restricciones de comercialización) y opera integrada a un sistema de facturación electrónica regulado por organismos fiscales. En este contexto, el sistema pasaría a manejar información con implicancias legales, fiscales y de seguridad pública.

Bajo esta declaración de criticidad, los estándares de cumplimiento obligatorio serían:

- **ISO/IEC 27001:** los registros de movimientos de materiales peligrosos, las relaciones con proveedores habilitados y los datos de acceso al sistema se convertirían en activos de información con valor legal. La norma exigiría: cifrado de credenciales y datos sensibles en tránsito y en reposo, logs de auditoría inmutables, gestión formal de incidentes de seguridad, control de acceso basado en el principio de mínimo privilegio, y planes de continuidad del negocio que garanticen la disponibilidad del sistema.
- **ISO 9001:** la trazabilidad completa de cada operación sobre materiales regulados sería exigida por organismos de control (OPDS, SENASA, AFIP según el tipo de material). Cada movimiento de stock debería asociarse a un documento respaldatorio (remito, factura) y ser auditable en cualquier momento por la autoridad competente.
- **ISA/IEC 62443:** si el sistema evolucionara para integrarse con sensores físicos de inventario, sistemas de pesaje conectados a la red, lectores de código de barras industriales o control de acceso electrónico al depósito de materiales peligrosos, este estándar aplicaría para la segmentación y protección de esa red de automatización.

ISO 13407 / ISO 9241-11, si bien no serían de cumplimiento obligatorio desde una perspectiva regulatoria, seguirían siendo obligatorias desde una perspectiva funcional: en un sistema crítico, un error de usabilidad que lleve a un operador a registrar una salida incorrecta de un material peligroso tiene consecuencias que van más allá del ámbito del software.

---

### 2.3. Conceptos de ISO 13407 e ISO 9241-11 vigentes en sistemas críticos

De **ISO 13407**, el concepto más perdurable y directamente aplicable a sistemas críticos es la evaluación iterativa con usuarios reales en condiciones representativas de uso. En sistemas críticos, este principio se convierte en un requisito no negociable: ningún sistema que controle procesos con consecuencias físicas, legales o de seguridad pública debería ser desplegado sin haber sido validado con los operadores reales que lo van a utilizar, bajo condiciones que repliquen las del entorno operativo. Las pruebas de usabilidad en laboratorio no son suficientes: es necesario validar bajo carga cognitiva real, en el entorno físico del operador y con datos representativos.

De **ISO 9241-11**, el concepto de eficacia —que el usuario logre completar correctamente la tarea— sigue siendo el indicador más crítico en cualquier dominio donde el error tiene consecuencias fuera del sistema. En sistemas de control industrial, financieros o de salud, la eficacia no es un atributo de calidad deseable sino una condición de seguridad: una interfaz que genera errores de operación en sus usuarios es, en sí misma, una vulnerabilidad del sistema, independientemente de cuán robusto sea el código subyacente.

---

## 3. Tabla Comparativa de Estándares

| **Estándar** | **Año** | **Enfoque principal** | **¿Aplica?** | **Justificación** |
|---|---|---|---|---|
| **ISO 9241-11** | 1998 (rev. 2018) | Usabilidad: define eficacia (logro de objetivos), eficiencia (recursos empleados) y satisfacción del usuario como dimensiones medibles de la interacción persona-sistema. | Sí, directamente | El sistema es operado a diario por empleados y encargados con distintos niveles de experiencia. La correcta carga de movimientos de stock depende de que la interfaz sea eficaz y eficiente. |
| **ISO 13407** | 1999 (reemplazada en 2010) | Proceso de Diseño Centrado en el Humano (HCD): cuatro etapas iterativas: comprensión del contexto de uso, especificación de requisitos, producción de soluciones de diseño, y evaluación. | Sí, como referencia metodológica | Sus etapas fueron aplicadas implícitamente en el TP1: se analizó el contexto operativo, se definieron flujos de uso y se refinaron pantallas iterativamente. |
| **ISO/IEC 27001** | 2005 (rev. 2022) | Sistema de Gestión de Seguridad de la Información (SGSI): gestión de riesgos, confidencialidad, integridad y disponibilidad de activos de información. | Parcialmente | El sistema gestiona credenciales, datos de stock e historial de movimientos. Presenta brechas críticas (credenciales en texto plano) que impiden su cumplimiento actual. |
| **ISA/IEC 62443** | 2007–presente | Ciberseguridad en sistemas de control industrial (OT): protección de redes SCADA, PLCs, HMIs y automatización de procesos físicos críticos. | No aplica actualmente | El sistema no controla equipamiento físico ni redes industriales. Aplicaría si se integraran sensores de inventario físico o control de acceso electrónico a depósitos. |
| **ISO 9001** | 1987 (rev. 2015) | Sistema de Gestión de la Calidad: ciclo PDCA (Planificar, Hacer, Verificar, Actuar), orientación a procesos, trazabilidad y mejora continua. | Sí, como marco de proceso | El ciclo de desarrollo (Sprint 0 → TP1 → TP2) refleja el ciclo PDCA. El historial de movimientos, el control de roles y la trazabilidad de operaciones son implementaciones directas de sus principios. |

---

## 4. Relación entre Decisiones de Diseño del TP1 y los Estándares

A continuación se analiza cómo cada decisión de diseño tomada en el TP1 facilita o dificulta el cumplimiento de los estándares estudiados.

| **Decisión de diseño (TP1)** | **Estándar relacionado** | **Relación** | **Análisis** |
|---|---|---|---|
| **Patrón Observer** (alertas de stock mínimo) | ISO/IEC 27001, ISO 9001 | Facilita | El mecanismo de notificación desacoplado puede extenderse para registrar eventos de seguridad y accesos anómalos sin alterar la lógica de negocio, alineándose con los controles de monitoreo de ISO 27001. |
| **Patrón Strategy** (movimientos: entrada, salida, ajuste) | ISO 9001, ISO/IEC 27001 | Facilita | Al aislar cada tipo de movimiento en una unidad independiente, se simplifica la auditoría individual de operaciones y se facilitan las pruebas unitarias, en línea con los principios de trazabilidad e integridad de datos. |
| **Borrado lógico** con campo `activo` | ISO 9001, ISO/IEC 27001 | Facilita | Garantiza que ningún dato sea eliminado físicamente de la base, preservando el historial completo del ciclo de vida de cada producto. Requisito explícito de trazabilidad en ISO 9001 y de disponibilidad de registros en ISO 27001. |
| **Control de acceso por rol** (encargado / empleado) | ISO/IEC 27001 | Facilita parcialmente | La estructura de roles existe y restringe operaciones críticas. Para cumplir ISO 27001 requeriría mayor granularidad, registro de intentos fallidos y revisión periódica de privilegios. |
| **Historial de movimientos** con usuario, fecha y motivo | ISO 9001, ISO/IEC 27001 | Facilita | Constituye la base de un log de auditoría funcional. Para ISO 27001 requeriría que estos registros sean inmutables y protegidos contra acceso no autorizado. |
| **Contraseñas en texto plano** | ISO/IEC 27001 | Dificulta gravemente | Constituye una no conformidad crítica. Debe resolverse reemplazando el almacenamiento directo por hashing con sal (bcrypt o equivalente) antes de cualquier intento de certificación. |

---

## 5. Conclusión — Certificación del Sistema

Si el equipo tuviera que certificar el sistema Stockeado bajo un estándar actual, elegiría **ISO/IEC 27001** como objetivo de certificación principal. Esta elección se fundamenta en que es el estándar que implicaría los cambios más estructurales y, por lo tanto, el que mayor valor agregaría al sistema desde una perspectiva de madurez técnica y confianza operacional. Los cambios concretos que requeriría la certificación son: reemplazar el almacenamiento de contraseñas en texto plano por hashing con sal (bcrypt o werkzeug.security); externalizar la `secret_key` de Flask a variables de entorno; implementar transacciones atómicas explícitas en todas las operaciones de escritura múltiple; hacer inmutables los registros del historial de movimientos; y agregar registro de eventos de acceso en una tabla de auditoría independiente. En términos de patrones, el **Observer** favorece el cumplimiento al permitir extender el mecanismo de notificación para emitir eventos de seguridad sin alterar la lógica central, y el **Strategy** facilita la auditoría independiente de cada tipo de operación, alineándose con el principio de integridad de datos que la norma exige.



*IS II · UCP Inc. · Eje 3 — HCI y Sistemas Críticos · 2026*
