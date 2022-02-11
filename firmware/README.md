# Firmware
## Funciones de prueba
Una vez construído nuestro SoC, tenemos a nuestra disposición todos los módulos construídos, para usarlos de la manera que definamos. Para aprovecharlos, debemos escribir el software que los va a controlar y de esta manera los pondrá a nuestra orden.

Para construir nuestro firmware, tenemos que tener claro cómo funcionan nuestros módulos y qué podemos leer y escribir de ellos. Sabiendo esto, Litex y Migen se han encargado de abstraer estos procesos mediante funciones generadas que se encuentran en el archivo [CSR.h](https://github.com/unal-edigital2-labs/wp08-2021-2-gr-06/blob/main/build/nexys4ddr/software/include/generated/csr.h) que podremos utilizar al escribir el programa que ejecutará nuestro SoC.

En nuestro caso, se escribieron funciones de prueba para cada módulo implementado con el objetivo de comprobar su respectiva operabilidad y, por supuesto, el programa principal con el cual el carro se encontrará en capacidad de recorrer un laberinto, reconocer su entorno y transmitir la información encontrada a un usuario por medio de la terminal y el modulo Bluethooth.

A continuación presentaremos las funciones integradas junto con sus respectivas explicaciones.

### test_ir()

```C
static void test_ir(void){
	while(!(buttons_in_read()&1)) {
		leds_out_write(infrarrojo_cntrl_distancia_read());
		delay_ms(50);
		}
}
```
En esta función vamos a presentar mediante los LED's integrados de la FPGA la lectura obtenida por el sensor infrarrojo en intervalos de 50ms hasta que presionemos un pulsador de su tablero.

### test_us()
```C
static void test_us(void){
	while(!(buttons_in_read()&1)) {
		ultrasonido_orden_write(1);
		bool done = false;
		while(!done){
			done = ultrasonido_done_read();
		}
		leds_out_write(ultrasonido_d_read());
		ultrasonido_orden_write(0);
		delay_ms(50);
		}
}
```
En esta función, haremos algo similar a lo hecho con nuestra prueba del funcionamiento del sensor infrarrojo, ahora con el sensor de ultrasonido. Este difiere en que el módulo de ultrasonido no tiene lecturas repetidas sino que se le debe dar la orden realizar todo el proceso relacionado con hacer la respectiva medición y de la misma manera establecer un reset para que este esté disponible para hacerla nuevamente.
### pwm_test()
```C
static void test_pwm(void){

	pwm_cntrl_orden_write(4);
	delay_ms(3000);
	pwm_cntrl_orden_write(5);
	delay_ms(3000);
	pwm_cntrl_orden_write(6);
	delay_ms(3000);
	pwm_cntrl_orden_write(4);
	delay_ms(500);
}
```
Con esta función, hacemos uso de la entrada "orden" previamente definida para el módulo PWM que nos permite girar un servomotor a -90°, 0° y 90°. 
### uart3_test()
```C
static void uart3_test(void){
	uart3_rxtx_write('A');
	printf("A");
	delay_ms(500);
}
```
En esta función, probaremos la UART que implementamos en pines arbitrarios de la FPGA, para ello, ponemos los respectivos pines de Rx y Tx en corto, pues probaremos de esta manera en la consola que tanto la escritura como la lectura de estos es correcta.
### rotate_car()
```C
void rotate_car(bool right){
	if (right){
		// Rotación a la derecha
		uart1_rxtx_write('J');
		delay_ms(350);
		uart1_rxtx_write('I');
		delay_ms(500);
	} else {
		// Rotación a la izquierda
		uart1_rxtx_write('H');
		delay_ms(350);
		uart1_rxtx_write('I');
		delay_ms(500);
	}
}
```
Esta función nos permite rotar el carro a la izquierda o a la derecha, para ello, hacemos uso de la UART1 que escribirá al Arduino la instrucción relacionada al giro de los motores con este fin. Al escribir la instrucción, le daremos un espacio de 350ms que es el tiempo que en nuestro caso resultó efctivo para realizar un giro adecuado y posteriormente detenemos todo el movimiento por 500ms para lograr una mayor estabilidad.
### forward()
```C
void forward(void){

	printf("Avanzando\n");
	uart1_rxtx_write('G');	
	while(infra_cntrl_output_infra_read() != 31){
		printf("Saliendo de la linea negra\n");
	}
		
	while(1) {
		printf("buscando linea negra\n");
		if (infra_cntrl_output_infra_read() < 31)
			break;
		
	}
	uart1_rxtx_write('I');
	
}
```
Con esta función, buscamos que el carro avance hasta encontrar una línea negra en el suelo dadas las condiciones que se nos fueron dadas para el laberinto. Para ello escribimos la señal de avanzar por medio de la UART1 al Arduino y de allí en adelante revisamos constantemente la salida provista por el sensor infrarrojo que, cuando detecte una distancia mayor a 2 (parámetro que nos entregó buenos resultados para detectar líneas negras), envíe la señal de alto para detener el movimiento.

```C
static void temhum_test(void){
	unsigned int temp[2];
	temp[0] = uart2_rxtx_read();
	printf("Temperatura: %d\n", temp[0]);
	temp[1] = uart2_rxtx_read();
	printf("Húmedad: %ld \n", temp[1]);
}
```
En esta fuinción se obtiene de manera individual el valor de la temperatura y la humedad obtenida por el UART del Arduino.

Todos los resultados se pueden ver en vídeo [aquí](https://drive.google.com/file/d/1VZ01Q7tJp9PNq_aDywC6H3XsN6wYvNeZ/view?usp=sharing).

## Programa principal  Recorrido del laberinto 
Antes de proceder con la explicación de nuestro algoritmo para recorrer el laberinto, recordaremos algunas condiciones y aspectos generales planteados.

 - El laberinto consiste cualquier recorrido donde solo sea posible una accion entre avanzar, girar a la izquierda o a la derecha.
 - El carro siempre tendrá una vía libre a la cual avanzar, de lo contrario, se asumirá que es el final del recorrido.
 - La información se presentará en un vector en la que la información en direcciones absolutas se presenta de la manera [UP, LEFT, DOWN].
 
Cabe recordar que este se encuentra adecuadamente comentado y en su totalidad en el archivo [main.c](https://github.com/unal-edigital2-labs/wp08-2021-2-gr-06/blob/main/firmware/main.c) de la carpeta firmware.


# ¿Cómo compilar y subir el firmware?
Una vez tenemos el firmware completamente escrito, tendremos que compilarlo en un archivo binario legible para el SoC. Este paso resulta sencillo debido a que es exactamente como compilar en el lenguaje C, además de que contamos con un archivo makefile por lo que el proceso que seguiremos inicia con asegurarnos de:
- Tener añadido el Path de Litex en la terminal
- Haber guardado todos los cambios en nuestros archivos de C.
Una vez hecho esto, abrimos una terminal en este directorio y ejecutamos el comando:
```ssh
make all
```
Comando que debe resultar sin errores y, una vez hecho esto, ya tenemos a nuestra disposición un archivo `firmware.bin` que podremos subir al SoC mediante la terminal de litex, abriendo una terminal en el directorio raíz del proyecto y ejecutando los comandos:
```ssh
sudo chmod 777 /dev/ttyUSB1
litex_term /dev/ttyUSB1 --kernel firmware/firmware.bin
```


