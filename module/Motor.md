## Motores

Los motores se conectaron por medio de un puente H a un Arduino Mega 2560. Se comunican a través del uart1 en donde dependiendo de la información recolectada por los sensores, estos girarán haciendo mover al carrito. Para ver el código completo puede acceder al siguiente link [Motores](/main/Arduino)

```
void loop () {

  if (Serial.available()){
    Motor_1 = Serial.read();
    if ( Motor_1 == 'I' )  {Parar (); }
    if ( Motor_1 == 'G' )  {Avanzar ();}
    if ( Motor_1 == 'H' )  {Izquierda (); }
    if ( Motor_1 == 'J' )  {Derecha (); }
    if ( Motor_1 == 'K' )  Atras ();
  }

}

```
En el archivo [main.c](/main/firmware/main.c) se declara la función **rotate_car** la cual recibe una variable booleana que determina la direccción del giro y envía el caracter correspondiente por el uart1 al arduino.
``` C
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
