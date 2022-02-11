# Robot Cartografo - Digital II - Grupo 6
## Autores
- Laura Manuela Castañeda Medina
- Migue Ángel Rodríguez Fuentes
- Daniel Felipe Torres Robles

Este es el repositorio del Robot Cartógrafo para la Asignatura de Electrónica Digital II de la Universidad Nacional de Colombia -  Sede Bogotá. El robot cartógrafo se realizó bajo una arquitectura de SoC, en una tarjeta de desarrollo Nexys A7, y periféricos los cuales sirven para cumplir el objetivo del proyecto, su funcionamiento principal radica en la generación de un vector donde se encuentran las direcciones del robot en cada instante de tiempo según el análisis del entorno en el que se encuentra por medio del sensor de ultrasonido, sensores infrarrojos y envio de datos por medio de bluetooth, y por otra parte se tiene un registro de la temperatura y humedad de las condiciones ambientales a las cuales esta sometido, siendo este nuestro periférico adicional.

![Screenshot](/Imágenes/Carro1.jpeg)

Como periféricos se implementaron un sensor de temperatura SHT31, un sensor infrarrojo seguidor de línea de 5 canales, 2 motores-reductores conectados a un puente H, un módulo bluetooth, un servo motor y un ultradonido HC-sr04. Se utilizó también un microprocesador Arduino Mega 2560 para realizar algunas conexiones y control de algunos procesos, los cuales se describirán más adelante. 

Se presenta un diagrama con las conexiones entre los diferentes periféricos y el SoC:
![Screenshot](/Imágenes/SoC.jpg)

El mapa de memoria se presenta a continuación.

<p align="center">
  <img src="/Imagenes/mem_bases.PNG" align="center">
</p>

## [Firmware](/Soc_project/firmware/) :
Se presenta la información del código usado para el desarrollo del funcionamiento del robot cartógrafo y principalmente el archivo [main.c](/firmware/main.c). 

## Periféricos :
En cada uno de los links se presenta el módulo en verilog y una explicación detallada del código utilizado para su funcionamiento.

- [Ultrasonido](/module/verilog/ultrasonido/)
- [Motores](/module/verilog/motor/)
- [Infrarrojos](/module/verilog/Infrarrojo/)
- [Sensor de Temperatura](Sensor)
- [Bluetooth](/Bluetooth/)
- [Arduino](/Arduino)

## Alimentación:
Se alimentan los periféricos a través de una extensión y un cargador de 5V/2A. El puente H se alimenta con 8 pilas AA para alcanzar los 12 voltios requeridos y la corriente que necesitan los motores para mover el carro. Debido a algunos inconvenientes con la alimentación de la FPGA y el Arduino, estos se conectan a los puertos USB del computador y se debe mover el computador según la ruta que siga el robot.

## Pruebas de Funcionamiento :
Se encuentra a continuación un enlace con los vídeos de funcionamiento de cada uno de los periféricos y el resultado final.

- [Detección infrarrojo]()
- [Ultrasonido/Giro Izquierda]()
- [Ultrasonido/Giro Derecha]()
- [Servomotor]()
- [Bluetooth]()
- [Sensor de Temperatura y Humedad]()
- [Resultado Final]()

