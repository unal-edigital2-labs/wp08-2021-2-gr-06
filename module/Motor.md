Los motores se conectaron por medio de un puente H a un Arduino Mega 2560. Se comunican a través del uart1 en donce dependiendo de la infromación recolectada por los sensores, estos girarán haciendo mover al carrito. 

````arduino
/////////////////////////////////////////////////////////
///// CONTROL MOTORES CARRITO EXPLORADOR - PUENTE H /////
/////////////////////////////////////////////////////////

// Motor 1
int ENA = 10;
int IN1 = 9;
int IN2 = 8;

// Motor 2
int ENB = 5;
int IN3 = 7;
int IN4 = 6;

// Control
char Motor_1 = 0;

void setup () {
  
  // PINES DE SALIDA - Puente H
  pinMode (ENA, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);
  
  // PINES DE ENTRADA - Control por Software  //   I   -   Parar
  pinMode (Motor_1, INPUT);                   //   G   -   Avanzar
                                              //   H   -   Izquierda
                                              //   J   -   Derecha
  Serial.begin(9600);
  Serial1.begin(9600);
                                              
}

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

void Avanzar () {

  //Direccion motor A
  digitalWrite (IN1, HIGH);
  digitalWrite (IN2, LOW);
  analogWrite (ENA, 95); //Velocidad motor A
  
  //Direccion motor B
  digitalWrite (IN3, HIGH);
  digitalWrite (IN4, LOW);
  analogWrite (ENB, 90); //Velocidad motor B

}

void Atras () {
  
  //Direccion motor A
  digitalWrite (IN1, LOW);
  digitalWrite (IN2, HIGH);
  analogWrite (ENA, 120); //Velocidad motor A
  
  //Direccion motor B
  digitalWrite (IN3, LOW);
  digitalWrite (IN4, HIGH);
  analogWrite (ENB, 120); //Velocidad motor B
  
}

void Derecha () {
  
  //Direccion motor A
  digitalWrite (IN1, HIGH);
  digitalWrite (IN2, LOW);
  analogWrite (ENA, 170); //Velocidad motor A
  
  //Direccion motor B
  digitalWrite (IN3, LOW);
  digitalWrite (IN4, HIGH);
  analogWrite (ENB, 170); //Velocidad motor B
  
}

void Izquierda () {
  
  //Direccion motor A
  digitalWrite (IN1, LOW);
  digitalWrite (IN2, HIGH);
  analogWrite (ENA, 255); //Velocidad motor A
  
  //Direccion motor B
  digitalWrite (IN3, HIGH);
  digitalWrite (IN4, LOW);
  analogWrite (ENB, 255); //Velocidad motor B
}


void Parar () {
  
  //Direccion motor A
  digitalWrite (IN1, LOW);
  digitalWrite (IN2, LOW);
  analogWrite (ENA, 0);   //Velocidad motor A
  
  //Direccion motor B
  digitalWrite (IN3, LOW);
  digitalWrite (IN4, LOW);
  analogWrite (ENB, 0);   //Velocidad motor B
  
}
```
``` c
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
