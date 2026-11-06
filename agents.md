PROYECTO A REALIZAR: Sistema administrativo de gestión automotriz
1. Registro de clientes
Nombre, correo y teléfono.
2. Registro de servicios
Vehículo, descripción, producto, marca, valor y fecha.
3. Buscar clientes
Buscar por nombre o teléfono.
4. Consultar historial
Mostrar los servicios registrados de un cliente.
5. Modificar o eliminar registros
Editar información del cliente o del servicio, adicional la funcion de eliminar un servicio.
6. Guardar información permanentemente
Conservar los datos al cerrar el programa.
7. Interfaz gráfica
Ventanas, botones y formularios con Tkinter. Presentación de interfaz moderna, colores o tonalidades oscuras. Al mostrar registros anteriores usar tablas.
8. Base de datos SQL
Almacenamiento mediante SQLite. Realizar tablas con datos guardados, tabla de clientes y tabla de servicios.

OBJETIVO GENERAL:
Diseñar, desarrollar, probar y documentar una aplicación utilizando los fundamentos esenciales del lenguaje de programación Python, demostrando capacidades de razonamiento lógico, resolución de problemas, organización del código y comprensión de las decisiones técnicas.
El proyecto simulará una prueba técnica para un desarrollador Python Junior. Se evaluará principalmente la comprensión de los fundamentos y no la complejidad de las tecnologías utilizadas.

1. Fundamentos mínimos que deben demostrarse
Independientemente de la temática seleccionada, el proyecto deberá proporcionar evidencias del uso y comprensión de los siguientes conceptos:
- Variables y tipos de datos: utilizar apropiadamente cadenas, números, booleanos u otros tipos necesarios.
- Operadores: aplicar operaciones aritméticas, comparaciones u operadores lógicos según el problema.
- Estructuras condicionales: utilizar if, elif o else para tomar decisiones.
- Bucles: utilizar for o while para realizar operaciones repetitivas.
- Estructuras de datos: demostrar el uso de listas, diccionarios, tuplas o conjuntos cuando resulten apropiados.
- Funciones: organizar la lógica en funciones reutilizables con parámetros y valores de retorno cuando corresponda.
- Validaciones: comprobar los datos de entrada y gestionar errores previsibles.
- Pruebas: verificar los resultados mediante casos de prueba representativos.
La programación orientada a objetos, los frameworks y las interfaces gráficas son opcionales. Su utilización no sustituye la demostración de los fundamentos anteriores.

2. Persistencia de datos: libertad tecnológica
El estudiante podrá seleccionar una o varias alternativas para almacenar y recuperar información, de acuerdo con las necesidades de su proyecto.
- TXT: archivos de texto plano.
- CSV: archivos con valores separados por comas.
- JSON: almacenamiento de datos estructurados.
- SQLite3: base de datos local.
- MySQL o PostgreSQL: bases de datos ejecutadas en Docker u otro entorno reproducible.
Regla de evaluación: no es obligatorio utilizar TXT, CSV, JSON, SQLite3 ni Docker específicamente. Se valorará que la alternativa elegida funcione y que el estudiante pueda explicar cómo almacena y recupera los datos.
Utilizar una tecnología más compleja no representa una ventaja automática en la calificación.

3. Desarrollo del proyecto
- Definición: identificar el problema, los usuarios potenciales y las funcionalidades principales.
- Diseño lógico: describir las entradas, procesos, salidas y estructuras de datos necesarias.
- Implementación: desarrollar el programa utilizando Python, funciones y estructuras adecuadas.
- Persistencia: implementar una solución que permita almacenar y recuperar los datos cuando la aplicación vuelva a ejecutarse.
- Validación: gestionar entradas incorrectas y situaciones excepcionales previsibles.
- Pruebas: ejecutar al menos tres casos: uno normal, uno límite y uno con datos incorrectos.
- Documentación: explicar las funcionalidades, los requisitos técnicos y las instrucciones de ejecución.

EVALUACION ADICIONAL:
Preguntas obligatorias de comprensión
El estudiante deberá responder las tres preguntas siguientes con sus propias palabras, tomando como referencia su proyecto. Las respuestas deberán incluirse en el archivo PDF de entrega.

Pregunta 1. Diseño y estructuras de datos (8 puntos)

¿Qué problema resuelve tu aplicación, cómo organizaste la solución y por qué elegiste las estructuras de datos utilizadas? Explica un ejemplo concreto de tu código.

Se evaluará la relación entre el problema, las estructuras utilizadas y la justificación técnica.

Pregunta 2. Lógica de programación (9 puntos)

Selecciona una función importante de tu aplicación y explica, paso a paso, cómo funciona. Indica qué papel cumplen las variables, los operadores, las condiciones y los ciclos que intervienen.

Se evaluará la comprensión del flujo de ejecución, la capacidad de explicación y la coherencia con el código.

Pregunta 3. Errores, pruebas y mejoras (8 puntos)

¿Qué sucede si tu programa recibe información incorrecta o encuentra un problema al guardar o recuperar los datos? Describe una prueba realizada, su resultado y una mejora que implementarías.

ENTREGABLES OBLIGATORIOS:
El estudiante deberá entregar un único archivo PDF a través de la plataforma educativa.

El PDF debe contener:

Nombre completo del estudiante.
Nombre del proyecto desarrollado.
Descripción breve del problema y la solución.
Enlace completo al repositorio público de GitHub.
Respuestas personales a las tres preguntas de comprensión.
Declaración del uso de herramientas de inteligencia artificial.
El repositorio de GitHub debe contener:

Código fuente completo del proyecto.
Archivo README.md con la documentación.
Dependencias necesarias, si corresponde.
Casos de prueba o evidencias reproducibles.
Archivos de configuración de ejemplo, cuando sean necesarios.
Archivo compose.yaml o equivalente si utiliza Docker.
El README.md deberá explicar: objetivo del proyecto, funcionalidades, tecnologías, requisitos, instalación, ejecución, almacenamiento de datos y pruebas realizadas.

El repositorio debe ser público, accesible y verificable sin solicitar permisos de acceso.

Seguridad: no publicar contraseñas, tokens, claves API, credenciales de bases de datos ni información personal sensible. Se pueden utilizar archivos .env.example con valores ficticios.

RÚBRICA DE EVALUACIÓN — 100 puntos
La evaluación considera el funcionamiento del proyecto, la aplicación de los fundamentos de Python, la documentación técnica y la comprensión demostrada por el estudiante.

Problema y diseño	Define un problema, establece funcionalidades y organiza la solución de forma coherente.	10
Funcionamiento	El programa se ejecuta correctamente y cumple las funcionalidades documentadas.	20
Fundamentos de Python	Utiliza correctamente variables, operadores, condicionales, ciclos, estructuras de datos y funciones.	18
Persistencia y validaciones	5 puntos: almacenamiento y recuperación funcional mediante TXT, CSV, JSON, SQLite3 o bases de datos en Docker.
5 puntos: validación de entradas y manejo de errores.	10
Pruebas y documentación	4 puntos: tres pruebas verificables.
4 puntos: README.md e instrucciones reproducibles.
4 puntos: repositorio público de GitHub y PDF correctamente entregado.	12
Comprensión personal	Responde las tres preguntas en el PDF con sus propias palabras, utilizando ejemplos reales de su código.
Pregunta 1: 8 puntos.
Pregunta 2: 9 puntos.
Pregunta 3: 8 puntos.	25
Uso crítico de herramientas e IA	Declara los recursos utilizados, explica las decisiones tomadas y demuestra que verificó los resultados obtenidos, con o sin IA.	5
TOTAL		100