# Robot Cartografo - Digital II - Grupo 6
## Autores
- Laura Manuela Castañeda Medina
- Migue Ángel Rodríguez Fuentes
- Daniel Felipe Torres Robles

Este es el repositorio del Robot Cartógrafo para la Asignatura de Electrónica Digital II de la Universidad Nacional de Colombia -  Sede Bogotá. El robot cartógrafo se realizó bajo una arquitectura de SoC, en una tarjeta de desarrollo Nexys A7, y periféricos los cuales sirven para cumplir el objetivo del proyecto, su funcionamiento principal radica en la generación de un vector donde se encuentran las direcciones del robot en cada instante de tiempo según el análisis del entorno en el que se encuentra por medio del sensor de ultrasonido, sensores infrarrojos y envio de datos por medio de bluetooth, y por otra parte se tiene un registro de la temperatura y humedad de las condiciones ambientales a las cuales esta sometido, siendo este nuestro periférico adicional.

![Screenshot](/Imagenes/robot.jpeg)

Como periféricos se implementaron un sensor de temperatura SHT31, un sensor infrarrojo seguidor de línea de 5 canales, 2 motores-reductores conectados a un puente H, un módulo bluetooth, un servo motor y un ultradonido HC-sr04. Se utilizó también un microprocesador Arduino Mega 2560 para realizar algunas conexiones y control de algunos procesos, los cuales se describirán más adelante. 

Se presenta un diagrama con las conexiones entre los diferentes periféricos y el SoC:
![Screenshot](/Imagenes/Diagrama.png)

El mapa de memoria se presenta a continuación.

<p align="center">
  <img src="/Imagenes/mem_bases.PNG" align="center">
</p>

## [SoC](/Soc_project/) :
Se realiza una descripción de la arquitectura del robot cartógrafo y el desaroolo en Litex para el ensamble y la integración del microprocesador picoRV32, el bus de datos Wishbone y los periféricos [Soc](/Soc_project/). 

## [Firmware](/Soc_project/firmware/) :man_technologist:
Se presenta la información del código usado para el desarrollo del funcionamiento del robot cartógrafo y principalmente el archivo [main.c](/Soc_project/firmware/main.c). 

## Periféricos :
En cada uno de los links se presenta el módulo en verilog y una explicación detallada del código utilizado para su funcionamiento.

- [Cámara](/Soc_project/module/verilog/camara/)
- [Radar](/Soc_project/module/verilog/ultrasonido/)
- [Motores](/Soc_project/module/verilog/motor/)
- [Infrarrojos](/Soc_project/module/verilog/infrarrojo/)
- [Sensor de Temperatura](/Soc_project/DFP_Player/)
- [Bluetooth](/Soc_project/Bluetooth/)
- [Arduino](/Arduino_Code_Cam_config/)

## Alimentación:
Se alimentan los periféricos a través de una extensión y un cargador de 5V/2A. El puente H se alimenta con 8 pilas AA para alcanzar los 12 voltios requeridos y la corriente que necesitan los motores para mover el carro. Debido a algunos inconvenientes con la alimentación de la FPGA y el Arduino, estos se conectan a los puertos USB del computador y se debe mover el computador según la ruta que siga el robot.

## Pruebas de Funcionamiento :
Se encuentra a continuación un enlace con los vídeos de funcionamiento de cada uno de los periféricos y el resultado final.

- [Resultado Final](https://drive.google.com/file/d/1Xd9sIncNKMFobtAyz-pI7O6QL3_JgV-1/view?usp=sharing)
- [Sensor de Temperatura](https://drive.google.com/file/d/1pixrffHi19yyft5Y8nsA9vXhZh5-91hg/view?usp=sharing)
- [Ultrasonido/Giro Derecha](https://drive.google.com/file/d/1ecpE0GoPpAQQU9fcsPIzm5rsk7ttgX0Z/view?usp=sharing)
- [Ultrasonido/Giro Izquierda](https://drive.google.com/file/d/1iYyBev4-YIb3iKXd45IIhB8J5pmOiLwX/view?usp=sharing)
- [Servomotor](https://drive.google.com/file/d/10o4X6v5wiUOjCU5KL25QMH4Qd_uEWAP3/view?usp=sharing)
- [Detección infrarrojo](https://drive.google.com/file/d/1VY-55Iuy-bAf_h2HWuiaHlmfi-5JuQ0W/view?usp=sharing)
