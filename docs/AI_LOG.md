
[AI_LOG (1) (1).md](https://github.com/user-attachments/files/26522096/AI_LOG.1.1.md)
# AI_LOG.md — Registro de uso de herramientas de IA

**Grupo:** Auras, Pelinski, Espínola, Mieres
**Proyecto:** Sistema de Inventario de Ferretería  
**Materia:** Ingeniería de Software II · UCP · 2026  

---

## Entradas del grupo (ordenadas por día y proceso de desarrollo)

---


## Entrada 001 — Semana 1

**Fecha:** 28/03/2026  
**Herramienta:** Claude  
**Responsable:** Scrum Master — Victoria Espinola  
**Eje temático:** Eje 1  

**¿Para qué se usó?**  
Definir la organización inicial del equipo, asignación de roles y planificación del sistema antes de comenzar el desarrollo.

**¿Qué generó la IA?**  
Una propuesta de división de roles (Scrum Master, Dev Lead, QA Lead, UX Lead), estructura de trabajo del equipo y sugerencias de organización de tareas por módulos del sistema.

**¿Qué aceptamos tal cual?**  
- La división de roles del equipo  
- La definición de responsabilidades por rol  
- La organización inicial del proyecto en módulos (login, productos, stock, alertas, importación)

**¿Qué modificamos y por qué?**  
- Ajustamos los nombres de los integrantes a los reales del grupo: se reemplazaron los nombres genéricos sugeridos por la IA  
- Refinamos las responsabilidades para alinearlas con el alcance académico del proyecto y evitar superposición de tareas  

**¿Qué descartamos y por qué?**  
Se descartó una planificación demasiado detallada tipo proyecto empresarial (roadmap extenso) porque excedía el alcance del trabajo práctico.

---

## Entrada 002 — Semana 1

**Fecha:** 29/03/2026  
**Herramienta:** Claude  
**Responsable:** Dev Lead — Lisandro Mieres  
**Eje temático:** Eje 2  

**¿Para qué se usó?**  
Diseñar el esquema completo de la base de datos relacional del sistema.

**¿Qué generó la IA?**  
Script SQL con 8 tablas, relaciones, claves foráneas, restricciones y datos iniciales.

**¿Qué aceptamos tal cual?**  
- Estructura completa de tablas  
- Uso de DECIMAL para precios  
- Campo `activo` para borrado lógico  
- Restricciones ON DELETE RESTRICT  
- Datos iniciales  

**¿Qué modificamos y por qué?**  
- Reordenamos la creación de tablas para evitar errores por dependencias  
- Agregamos `utf8mb4` para soportar caracteres especiales  

**¿Qué descartamos y por qué?**  
Nada  

---

## Entrada 003 — Semana 2

**Fecha:** 31/03/2026  
**Herramienta:** Claude  
**Responsable:** Dev Lead — Lisandro Mieres  
**Eje temático:** Eje 2  

**¿Para qué se usó?**  
Implementar login y autenticación.

**¿Qué generó la IA?**  
Backend en Flask con sesiones y control por rol.

**¿Qué aceptamos tal cual?**  
- Función login  
- Uso de session  
- Redirección por rol  
- Logout  

**¿Qué modificamos y por qué?**  
- Validación de usuario activo  
- Separación de config en archivo externo  

**¿Qué descartamos y por qué?**  
Nada  

---

## Entrada 004 — Semana 2

**Fecha:** 01/04/2026  
**Herramienta:** Claude  
**Responsable:** UX Lead — Emilia Auras  
**Eje temático:** Eje 3  

**¿Para qué se usó?**  
Diseñar interfaz del login.

**¿Qué generó la IA?**  
HTML + CSS responsive con estilos modernos.

**¿Qué aceptamos tal cual?**  
- Formulario  
- Estilos base  
- Diseño centrado  
- Efectos visuales  

**¿Qué modificamos y por qué?**  
- Mensaje de error dinámico  
- Colores institucionales  

**¿Qué descartamos y por qué?**  
Nada  

---

## Entrada 005 — Semana 2

**Fecha:** 01/04/2026  
**Herramienta:** Claude  
**Responsable:** Dev Lead — Lisandro Mieres  
**Eje temático:** Eje 2  

**¿Para qué se usó?**  
Implementar gestión de productos.

**¿Qué generó la IA?**  
Frontend + rutas backend para CRUD.

**¿Qué aceptamos tal cual?**  
- Formulario  
- Tabla de listado  
- Búsqueda y filtros  
- Uso de JOIN  

**¿Qué modificamos y por qué?**  
- Filtro por activos  
- Borrado lógico  
- Indicadores visuales de stock  

**¿Qué descartamos y por qué?**  
Eliminación física de productos (rompe trazabilidad)  

---

## Entrada 006 — Semana 2

**Fecha:** 02/04/2026  
**Herramienta:** Claude  
**Responsable:** Dev Lead — Lisandro Mieres  
**Eje temático:** Eje 2  

**¿Para qué se usó?**  
Implementar alertas automáticas (Observer).

**¿Qué generó la IA?**  
Lógica de detección de stock bajo.

**¿Qué aceptamos tal cual?**  
- Verificación automática  
- Inserción de alertas  
- Resolución manual  

**¿Qué modificamos y por qué?**  
- Evitar alertas duplicadas  
- Mejorar mensajes  

**¿Qué descartamos y por qué?**  
Resolución automática de alertas  

---

## Entrada 007 — Semana 2

**Fecha:** 02/04/2026  
**Herramienta:** Claude  
**Responsable:** Dev Lead — Lisandro Mieres  
**Eje temático:** Eje 2  

**¿Para qué se usó?**  
Implementar movimientos de stock (Strategy).

**¿Qué generó la IA?**  
Lógica condicional para entrada, salida y ajuste.

**¿Qué aceptamos tal cual?**  
- Separación por tipo  
- Validación de stock  
- Actualización  

**¿Qué modificamos y por qué?**  
- Campo motivo  
- Mensajes de error claros  

**¿Qué descartamos y por qué?**  
Nada  

---

## Entrada 008 — Semana 2

**Fecha:** 03/04/2026  
**Herramienta:** Claude  
**Responsable:** UX Lead — Emilia Auras  
**Eje temático:** Eje 3  

**¿Para qué se usó?**  
Rediseño UI completo.

**¿Qué generó la IA?**  
Tema claro/oscuro + iconos + navbar unificada.

**¿Qué aceptamos tal cual?**  
- Iconos  
- Tema persistente  
- Variables CSS  

**¿Qué modificamos y por qué?**  
- Orden de scripts  
- Validaciones JS  
- Estilos completos  

**¿Qué descartamos y por qué?**  
Nada  

---

## Entrada 009 — Semana 2

**Fecha:** 03/04/2026  
**Herramienta:** Claude  
**Responsable:** Dev Lead — Lisandro Mieres  
**Eje temático:** Eje 2  

**¿Para qué se usó?**  
Importación de Excel de proveedores.

**¿Qué generó la IA?**  
Procesamiento de Excel + interfaz de decisiones.

**¿Qué aceptamos tal cual?**  
- openpyxl  
- Búsquedas  
- Actualización automática  

**¿Qué modificamos y por qué?**  
- Procesamiento masivo  
- Vinculación de productos  
- Validaciones  

**¿Qué descartamos y por qué?**  
Soporte CSV innecesario  

---

## Entrada 010 — Semana 2

**Fecha:** 03/04/2026  
**Herramienta:** Claude  
**Responsable:** QA Lead — Matías Pelinski  
**Eje temático:** Eje 2  

**¿Para qué se usó?**  
Corregir roles de usuario.

**¿Qué generó la IA?**  
Scripts SQL y ajustes en código.

**¿Qué aceptamos tal cual?**  
- SQL de actualización  
- Validaciones por rol  

**¿Qué modificamos y por qué?**  
- Uso de valor temporal para evitar pérdida de datos  
- Simplificación visual  

**¿Qué descartamos y por qué?**  
Nada  

---

## Entrada 011 — Semana 2

**Fecha:** 03/04/2026  
**Herramienta:** Claude  
**Responsable:** Scrum Master — Victoria Espinola  
**Eje temático:** Eje 3  

**¿Para qué se usó?**  
Generar diagrama de casos de uso.

**¿Qué generó la IA?**  
Diagrama + tabla de casos.

**¿Qué aceptamos tal cual?**  
- Actores  
- Casos principales  
- Estructura  

**¿Qué modificamos y por qué?**  
- Eliminamos interacción directa proveedor-sistema  
- Agregamos caso faltante  

**¿Qué descartamos y por qué?**  
Relaciones innecesarias (include/extend)  

---

## Roles del equipo

- **Scrum Master — Victoria Espinola**  
  Coordina el equipo, organiza tareas, define prioridades y valida el cumplimiento del proceso.

- **Dev Lead — Lisandro Mieres**  
  Diseña la arquitectura del sistema, implementa la lógica de negocio y supervisa el desarrollo técnico.

- **QA Lead — Matías Pelinski**  
  Verifica la calidad del sistema, realiza pruebas, detecta errores y valida los resultados.

- **UX Lead — Emilia Auras**  
  Diseña la interfaz de usuario, mejora la experiencia de uso y asegura la coherencia visual del sistema.

---
## Entrada 012 — Semana 3

**Fecha:** 18/04/2026
**Herramienta:** Claude (Anthropic) — claude.ai
**Responsable:** Scrum Master — Victoria Espínola
**Eje temático:** Eje 3 — HCI y Sistemas Críticos

**¿Para qué se usó?**
Desarrollar el análisis completo de estándares de validación de sistemas (HCI y sistemas críticos) requerido por la consigna del Eje 3.

**¿Qué generó la IA?**
Documento completo `ANALISIS_ESTANDARES.md` con investigación de ISO 9241-11, ISO 13407, ISO/IEC 27001, ISA/IEC 62443 e ISO 9001; tabla comparativa; análisis aplicado al escenario de ferretería; conclusión sobre certificación; y tabla de relación entre decisiones de diseño del TP1 y los estándares.

**¿Qué aceptamos tal cual?**
- Estructura general del documento
- Descripción técnica de cada estándar
- Tabla comparativa con los 5 estándares
- Análisis de relevancia por escenario
- Conclusión sobre ISO/IEC 27001 como estándar a certificar
- Tabla de relación con patrones Observer y Strategy del TP1

**¿Qué modificamos y por qué?**
Se verificó la coherencia con las decisiones reales del TP1 (patrones implementados, estructura de base de datos, roles de usuario) para asegurar que el análisis refleje el sistema real del grupo y no uno genérico.

**¿Qué descartamos y por qué?**
Referencias a estándares fuera de la consigna y ejemplos de otros dominios no aplicables al escenario de ferretería.
---

## Resumen de entradas

| Entrada | Semana | Eje | Descripción |
|--------|--------|-----|------------|
| 001 | 4 | Eje 1 | Organización del equipo |
| 002 | 4 | Eje 2 | Base de datos |
| 003 | 4 | Eje 2 | Login |
| 004 | 4 | Eje 3 | UI Login |
| 005 | 4 | Eje 2 | Productos |
| 006 | 5 | Eje 2 | Alertas |
| 007 | 5 | Eje 2 | Movimientos |
| 008 | 5 | Eje 3 | UI general |
| 009 | 5 | Eje 2 | Excel |
| 010 | 5 | Eje 2 | Roles |
| 011 | 5 | Eje 3 | Casos de uso |
| 012 | 6 | Eje 3 | Análisis de estándares HCI y sistemas críticos |
---
