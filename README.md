## MI LINKEDIN:
https://www.linkedin.com/in/ismael-qui%C3%B1ones-gama-0328b9243/

# TFG (SALIBANK)
Aquí puede encontrarse el código de mi trabajo de fin de grado (TFG). El TFG consiste en la creación de un prototipo para una máquina de recolección de muestras de saliva para posterior análisis en laboratorio. La nota recibida en el TFG fue de Sobresaliente. El resumen del trabajo es el siguiente:

## RESUMEN:
Durante la pandemia que hemos estado viviendo se han realizado una gran cantidad de tests en los centros de salud, realizados por personal médico, para seguir de cerca la incidencia de la COVID-19 en la sociedad y poder actuar en consonancia. Todos los millones de test realizados comportan un problema: Se está destinando personal médico a realizar esa función, dejando huecos en la atención primaria. En este trabajo de fin de grado se propone un sistema hardware para una máquina de autoservicio que pueda utilizar la población para realizar tests de saliva que puedan ser analizados posteriormente en laboratorios. La máquina sería válida tanto en la actual pandemia, ya que la COVID es detectable por vía salival, como en otras infecciones como hepatitis, VIH, bacterias diversas, marcadores tumorales, etc. El sistema que este documento describe es capaz de identificar a un usuario y dispensar un kit para que pueda realizar una prueba de saliva. Cuando el usuario haya realizado la prueba, podrá introducir su muestra de saliva en la propia máquina. La máquina, aparte de realizar las acciones ya comentadas, se encarga de asociar, en una base de datos, al paciente en cuestión con su muestra entregada. Así, posteriormente, en el laboratorio, será una tarea rápida la asociación de un ciudadano con una cierta muestra analizada. El sistema está compuesto por un microprocesador gobernando el módulo central y dos microcontroladores, conectados al central, gobernando los módulos de recolectar y dispensar. Al módulo central también va conectada una pantalla sobre la que se muestra la aplicación y puede interactuar el usuario, así como una impresora de etiquetas y un lector de código de barras, y a los módulos laterales van conectados un relé, un motor y unos sensores de temperatura e infrarojos, con las funciones de monitorear y comprobar el correcto funcionamiento del sistema, así como para cerrar lazos de control. 

## MÓDULOS DE LA MÁQUINA:
Es un sistema modular que cuenta con 3 módulos. La idea de la modularidad viene motivada por que se puedan hacer cambios y adaptaciones que involucren a un módulo sin que se tengan que tocar los demás, abaratando costes.

### MÓDULO CENTRAL:
El módulo central estará conectado a internet para poder comunicar a Operadores problemas de la máquina y para poder comunicarse con una base de datos remota. Estará compuesto por una Raspberry, conectada a los Arduinos de los módulos latereales, A un lector de códigos de barras (para identificar al usuario) y a una impresora de etiquetas (para imprimir identificativos de muestras de saliva).

### MÓDULO DISPENSADOR:
El módulo dispensador será un módulo esclavo cuya función será entregar kits para realizar muestras al usuario cuando este necesite. Estará formado por un motor conectado a un tornillo sin fin (como las máquinas de vending), así como un sensor IR para detectar la caída de la muestra y detener el motor (si esto fallase, una interrupción hardware lo detendría), un relé para cortar o permitir el paso de la alimentación externa al motor y un Arduino (conectado a la Raspberry) para gobernar este módulo.

### MÓDULO RECOLECTOR:
El módulo recolector será un módulo esclavo cuya función será recoger muestras del usuario para que luego puedan ser recogidas por un operario. También será el encargado de proporcionar la temperatura al módulo central cada vez que éste se la pida (temperatura a la que están siendo expuestas las muestras del contenedor). Está formado por un Arduino, un sensor IR (que detecta la entrada de muestra) y un sensor de temperatura.

## VÍDEOS DE FUNCIONAMIENTO:

USO DEL SISTEMA POR PARTE DE UN USUARIO:
https://drive.google.com/file/d/1Rlp5J5qqJrmmmDmw3DvSVwc0Yt33LZVe/view?usp=sharing

USO DEL SISTEMA POR PARTE DE UN OPERADOR O ADMINISTRADOR:
https://drive.google.com/file/d/10E1s1bws7V3OXz6RXL2Z-sKkVkkqbEYG/view?usp=sharing

## MEMORIA TRABAJO:

MEMORIA:
https://drive.google.com/file/d/1aCXYzBCFqEmjF4RBp85nQ_s09-SaJaHo/view?usp=sharing

ANEXOS:
https://drive.google.com/file/d/1x0ZabSHlSAeVmOO3gmqft1LFoOMU1mC0/view?usp=sharing
