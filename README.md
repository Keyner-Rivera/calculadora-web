Calculadora Web de Raíces de Funciones
Este proyecto es una aplicación web interactiva diseñada para el cálculo de raíces de funciones utilizando métodos numéricos. Desarrollada con Django y Python en un entorno virtual, esta herramienta ofrece una forma eficiente de resolver ecuaciones no lineales, visualizando tanto el proceso como los resultados.
Funcionalidades Destacadas
Cálculo de Raíces: Permite encontrar las raíces de una función ingresada por el usuario a través de los métodos de Bisección, Newton-Raphson y Newton-Raphson Modificado.
Interfaz de Usuario: Una interfaz limpia e intuitiva que facilita la introducción de funciones y parámetros.
Campos Dinámicos: Los campos del formulario se ajustan automáticamente según el método numérico seleccionado, mostrando solo la información relevante.
Visualización Gráfica: Genera una gráfica de la función para proporcionar una representación visual de la raíz encontrada.
Historial de Cálculos: Mantiene un registro detallado de todas las operaciones realizadas, incluyendo los parámetros utilizados y los resultados obtenidos.
Detalle de Iteraciones: Presenta una tabla con el desglose de cada iteración del algoritmo, mostrando la convergencia hacia la raíz.
Validación y Manejo de Errores: Incluye validaciones robustas para las entradas del usuario y mensajes claros en caso de errores o falta de convergencia.
Tecnologías Empleadas
Backend: Python (lenguaje de programación) y Django (framework web).
Frontend: HTML5, CSS3 y JavaScript para la estructura, el estilo y la interactividad de la interfaz.
Entorno de Desarrollo: Se utiliza un entorno virtual para gestionar las dependencias de Python de forma aislada.
Configuración y Puesta en Marcha
Para ejecutar este proyecto en tu entorno local, sigue los siguientes pasos:

1. Clonar el Repositorio
Bash
git clone <URL_DEL_REPOSITORIO>
cd calculadora-raices-web
2. Configurar el Entorno Virtual
Se recomienda encarecidamente utilizar un entorno virtual para aislar las dependencias del proyecto.

En Windows:
Bash
python -m venv venv
.\venv\Scripts\activate
En macOS/Linux:

Bash
python3 -m venv venv
source venv/bin/activate
3. Instalar Dependencias
Con el entorno virtual activado, instala las bibliotecas necesarias. Asegúrate de tener un archivo requirements.txt en la raíz del proyecto con las dependencias (ej., Django, numpy, sympy, matplotlib).

Bash
pip install -r requirements.txt
4. Ejecutar Migraciones de la Base de Datos
Bash

python manage.py migrate
5. Iniciar el Servidor de Desarrollo
Bash

python manage.py runserver
6. Acceder a la Aplicación
Una vez que el servidor esté en funcionamiento, abre tu navegador web y navega a:

http://127.0.0.1:8000/

Modo de Uso
Ingresar Función: Introduce la expresión matemática en el campo de "Función", utilizando x como variable (por ejemplo, x**3 - 2*x - 5).
Seleccionar Método: Elige el método numérico deseado del menú desplegable.
Definir Parámetros: Proporciona los valores requeridos para el método seleccionado (intervalo [a, b] para Bisección; suposición inicial x₀ y derivadas para Newton-Raphson).
Ajustar Criterios: Establece la tolerancia y el número máximo de iteraciones para el cálculo.
Calcular: Haz clic en el botón "Calcular" para obtener la raíz.
Revisar Resultados: Los resultados, la gráfica de la función, el detalle de las iteraciones y el historial de cálculos se mostrarán en la página.
