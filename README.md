# TFG (SALIBANK)
Aquí puede encontrarse el código de mi trabajo de fin de grado (TFG). El TFG consiste en la creación de un prototipo para una máquina de recolección de muestras de saliva para posterior análisis en laboratorio.

Es un sistema modular que cuenta con 3 módulos:

## MÓDULO CENTRAL:
El módulo central estará conectado a internet para poder comunicar a Operadores problemas de la máquina y para poder comunicarse con una base de datos remota. Estará compuesto por una Raspberry, conectada a los Arduinos de los módulos latereales, A un lector de códigos de barras (para identificar al usuario) y a una impresora de etiquetas (para imprimir identificativos de muestras de saliva).

## MÓDULO DISPENSADOR:
El módulo dispensador será un módulo esclavo cuya función será entregar kits para realizar muestras al usuario cuando este necesite. Estará formado por un motor conectado a un tornillo sin fin (como las máquinas de vending), así como un sensor IR para detectar la caída de la muestra y detener el motor (si esto fallase, una interrupción hardware lo detendría), un relé para cortar o permitir el paso de la alimentación externa al motor y un Arduino (conectado a la Raspberry) para gobernar este módulo.

## MÓDULO RECOLECTOR:
El módulo recolector será un módulo esclavo cuya función será recoger muestras del usuario para que luego puedan ser recogidas por un operario. También será el encargado de proporcionar la temperatura al módulo central cada vez que éste se la pida (temperatura a la que están siendo expuestas las muestras del contenedor). Está formado por un Arduino, un sensor IR (que detecta la entrada de muestra) y un sensor de temperatura.

## VÍDEOS DE FUNCIONAMIENTO:

USO DEL SISTEMA POR PARTE DE UN USUARIO:
https://drive.google.com/file/d/1Rlp5J5qqJrmmmDmw3DvSVwc0Yt33LZVe/view?usp=sharing

USO DEL SISTEMA POR PARTE DE UN OPERADOR O ADMINISTRADOR:
https://drive.google.com/file/d/10E1s1bws7V3OXz6RXL2Z-sKkVkkqbEYG/view?usp=sharing

## La memoria de este trabajo puede ser encontrada aquí:

MEMORIA:
https://drive.google.com/file/d/1aCXYzBCFqEmjF4RBp85nQ_s09-SaJaHo/view?usp=sharing

ANEXOS:
https://drive.google.com/file/d/1x0ZabSHlSAeVmOO3gmqft1LFoOMU1mC0/view?usp=sharing
