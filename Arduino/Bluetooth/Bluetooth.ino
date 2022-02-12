//codigo del Bluetooth
//COM 7

#include "BluetoothSerial.h"

#define RXD2 16
#define TXD2 17

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

char dato;

void setup() {
  Serial.begin(9600);
  SerialBT.begin("ESP32test"); //Nombre del Bluetooth
  Serial.println("The device started, now you can pair it with bluetooth!");
  Serial2.begin(9600,SERIAL_8N1,RXD2,TXD2);
}

void loop() {
  if (Serial2.available()) { //Encuentra algo en el Rx
   dato = Serial.read();     //Guarda el dato disponible en el Puerto serial
   SerialBT.write(dato);    //Manda el dato por Bluetooh
   Serial.print(dato);     //Muestra el dato en el Serial del ESP32
  }
}
