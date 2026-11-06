# Sistema de gestión automotriz

Aplicación de escritorio para administrar clientes y los servicios asociados a
sus vehículos. Está construida con Python, Tkinter y SQLite.

## Alcance y criterios de aceptación

### Clientes

- Registrar clientes con nombre, correo y teléfono obligatorios.
- Buscar por coincidencias parciales en el nombre o el teléfono.
- Seleccionar un resultado, cargar sus datos en el formulario y modificarlo.
- Mostrar la lista completa al abrir la pestaña y volver a ella con **Mostrar
  todos**.
- Eliminar un cliente sin servicios asociados después de confirmar. Si tiene
  servicios, se bloquea el borrado para conservar el historial. Al borrar un
  cliente, los IDs restantes se compactan y sus servicios siguen vinculados.
  El siguiente cliente recibe el ID consecutivo.
- Rechazar campos vacíos o que no sean texto y mostrar errores comprensibles.
- El teléfono celular debe contener exactamente 10 dígitos; se conserva como
  texto para no perder ceros iniciales.
- No se exige un formato específico para el correo.

### Servicios e historial

- Registrar un servicio asociado a un cliente existente con vehículo,
  descripción del problema, producto, valor y fecha.
- Rechazar texto obligatorio vacío. El valor debe ser numérico, finito y mayor
  o igual a cero; se permiten servicios gratuitos.
- Ingresar la fecha como `DD/MM/AAAA`; se valida como fecha real y se almacena
  como `AAAA-MM-DD`.
- Consultar los servicios del cliente seleccionado del más reciente al más
  antiguo.
- Seleccionar un servicio para cargarlo en el formulario y modificarlo sin
  cambiar el cliente asociado.
- Solicitar confirmación antes de eliminar un servicio. Los IDs inexistentes
  producen errores explícitos. Después de borrar un servicio, los IDs
  restantes se compactan para que no queden saltos.

### Persistencia e interfaz

- Crear las tablas SQLite al iniciar si todavía no existen, sin eliminar los
  registros ya guardados.
- Mantener los datos localmente en `datos/automotriz.db`.
- Migrar la tabla existente de servicios para retirar el campo marca sin perder
  los datos históricos.
- Separar clientes y servicios en pestañas Tkinter, mostrar registros e
  historiales en tablas y usar una presentación oscura.
- Mostrar en la interfaz los errores de validación y almacenamiento.

## Requisitos

- Python 3.8 o posterior.
- Tkinter disponible en la instalación de Python.

El proyecto utiliza la biblioteca estándar de Python y no requiere instalar
paquetes externos.

## Ejecución y uso

Desde la carpeta raíz del proyecto, ejecuta:

```text
python main.py
```

La aplicación crea la base y sus tablas si es el primer inicio.

1. En **Clientes** aparece la lista completa al abrir la pestaña. Completa
   nombre, correo y teléfono (exactamente 10 dígitos) y pulsa **Guardar cliente**.
2. Para encontrar un cliente en una lista extensa, escribe su nombre o teléfono
   en el campo de búsqueda y pulsa **Buscar**. Pulsa **Mostrar todos** para
   volver a la lista completa. Selecciona una fila para cargar sus datos;
   luego pulsa **Modificar seleccionado** para guardar cambios o
   **Eliminar seleccionado** para borrar. Para proteger el historial, no se
   permite borrar clientes que tengan servicios asociados. **Limpiar** vacía
   el formulario.
3. En **Servicios**, selecciona un cliente en la lista. Su historial aparece
   en la tabla. Si acabas de registrar un cliente y no aparece, pulsa
   **Actualizar clientes**. La lista se sincroniza también al abrir esta
   pestaña, así que los clientes eliminados ya no quedan como opciones.
4. Completa los datos del servicio y pulsa **Guardar servicio**. La descripción
   del problema admite varias líneas. Ingresa el valor como número (usa punto
   para los decimales) y la fecha como `DD/MM/AAAA`.
5. Selecciona una fila del historial para cargar el servicio. Usa
   **Modificar seleccionado** para actualizarlo o **Eliminar seleccionado**
   para borrarlo después de confirmar. La edición conserva el cliente
   seleccionado.

## Datos y validaciones

- Los campos de cliente y servicio son obligatorios y no pueden contener solo
  espacios.
- El nombre, correo y teléfono se guardan como texto. El teléfono celular debe
  contener exactamente 10 dígitos.
- No se impone un formato específico para el correo.
- El valor no puede ser negativo ni infinito; cero está permitido.
- La fecha debe existir en el calendario y se muestra en formato `DD/MM/AAAA`.
- Cada servicio debe referenciar a un cliente existente.
- Los datos persisten al cerrar la aplicación. La base local no se incluye en
  Git.

## Pruebas

Ejecuta las pruebas automatizadas con:

```text
python -m unittest discover -s tests -v
```

Las pruebas usan bases temporales para no alterar los datos de la aplicación.

## Estructura del proyecto

```text
main.py         Punto de entrada
README.md       Uso, criterios de aceptación y documentación
agents.md       Requisitos y entregables del proyecto
.progress       Checklist del avance
.gitignore      Exclusiones de Git
clientes/       Registro, modificación y consultas de clientes
servicios/      Registro, modificación, eliminación e historial
interfaz/       Ventanas, formularios y tablas Tkinter
datos/          Módulo SQLite y base local creada al iniciar
validaciones/   Validaciones compartidas
tests/          Pruebas automatizadas con unittest
```

## Uso de inteligencia artificial

Se utilizó GitHub Copilot como apoyo para explicar conceptos, revisar la
estructura y desarrollar partes del código y de las pruebas. El proyecto debe
ser revisado y comprendido por la estudiante, quien explicará las decisiones y
los resultados con sus propias palabras en la entrega.

## Referencia del curso

Los conceptos de Python aplicados en el proyecto se estudian en el
[Ebook oficial Programación en Python + AI](https://statick88.github.io/Course_of_python/).
