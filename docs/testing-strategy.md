## B3. Diseño conceptual de pruebas de integración

### a. Identificación de dos dependencias externas

Para que las pruebas de integración sean efectivas, debemos identificar aquellos componentes que están fuera del control directo de nuestras funciones en Python y cuya falla o ausencia impediría la ejecución completa del flujo. Se han identificado dos dependencias críticas:

**1. Motor de base de datos relacional (MySQL / MariaDB)**  
- **Naturaleza:** infraestructura externa que se comunica con la aplicación mediante TCP/IP (red o sockets locales).  
- **Impacto en la integración:** el sistema depende de la disponibilidad del servidor de base de datos, de la integridad del esquema (tablas `productos`, `usuarios`, `movimientos_stock`) y de la persistencia de los datos. Una prueba de integración debe verificar no solo que el código Python es correcto, sino que las sentencias SQL —por ejemplo, el cálculo de stock en `registrar_movimiento`— interactúan correctamente con las restricciones y tipos de datos definidos en el motor.

**2. Sistema de archivos y persistencia en disco (módulo `os` y directorio `uploads`)**  
- **Naturaleza:** dependencia del sistema operativo que gestiona la lectura y escritura de archivos físicos.  
- **Impacto en la integración:** la funcionalidad de importación de archivos Excel utiliza la librería `openpyxl` para leer documentos almacenados en la carpeta `uploads`. La prueba de integración debe validar que la aplicación tenga los permisos de escritura necesarios, que el archivo se guarde correctamente después de ser subido y que sea eliminado (limpieza de temporales) una vez procesado el Excel del proveedor.

### b. Explicación de cómo se mockearían/stubearían en una prueba futura

**¿Qué significa “mockear” en las pruebas de software?**  
El término *mock* (simular, imitar) se refiere a una técnica fundamental en el control de calidad que consiste en reemplazar dependencias externas reales —bases de datos, APIs de terceros, red, sistema de archivos— por objetos simulados controlados durante la ejecución de pruebas automatizadas.

En las pruebas de integración, muchas veces necesitamos aislar el comportamiento de la aplicación para no depender de la infraestructura externa. Por ejemplo, no queremos levantar un servidor MySQL real cada vez que se ejecutan las pruebas en GitHub Actions. El objetivo de utilizar estos *dobles de prueba* es garantizar que los tests tengan tres características clave:  
- **Determinismo:** el resultado siempre es el mismo, porque no depende del estado cambiante de una base de datos o de la red.  
- **Velocidad:** se evita la sobrecarga de tiempo que implica iniciar infraestructura real o realizar operaciones pesadas de entrada/salida (I/O).  
- **Independencia:** se prueba la lógica de negocio sin riesgo de que factores externos (servidor caído, falta de permisos en disco) generen falsos negativos.

A partir de este concepto, aplicaremos dos enfoques distintos según lo que necesitemos evaluar en el sistema:

#### 1. Stubbing de la base de datos (pruebas basadas en estado)
- **Concepto:** un *Stub* es un objeto que devuelve respuestas predefinidas (*enlatadas*) a las llamadas que se realizan durante la prueba. Sirve para simular el estado del sistema.  
- **Aplicación:** para probar la ruta `/productos`, en lugar de consultar la base de datos real, *stubeamos* la función `get_db_connection()`. Cuando el código solicite la lista de productos, el Stub devolverá un diccionario estático como:  
  ```python
  [{'id': 1, 'nombre': 'Martillo', 'stock_actual': 5, 'stock_minimo': 10}]
  ```  
  Esto permite verificar que el frontend y la lógica de Python procesan y muestran correctamente los datos, sin depender de que la base esté vacía o caída.

#### 2. Mocking de componentes de entrada/salida (pruebas basadas en interacción)
- **Concepto:** un *Mock* es un objeto más complejo que no solo devuelve datos, sino que registra cómo fue llamado (cuántas veces, con qué argumentos, en qué orden). Se utiliza para verificar el comportamiento y la interacción entre componentes.  
- **Aplicación:** al probar la carga de facturas de proveedores, *mockeamos* el objeto `request.files['archivo']`. No necesitamos un archivo `.xlsx` real en disco. El Mock verificará que la lógica de la función `importar()` llame efectivamente al método `.save()` con la ruta de destino correcta. Si el método no es invocado, el Mock hace que la prueba falle, asegurando que la integración con el sistema de archivos se realice según lo esperado.

**Herramienta gratuita recomendada**  
Se propone utilizar **`unittest.mock`** (biblioteca estándar de Python). Es la opción ideal porque permite crear mocks y stubs sin dependencias externas, se integra perfectamente con pytest y cubre los dos escenarios descritos: simular el conector de base de datos e interceptar interacciones con el sistema de archivos.

---
