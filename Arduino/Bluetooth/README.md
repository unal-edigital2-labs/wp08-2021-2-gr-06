## Bluetooth

Para la comunicación por Bluetooth, se hizo uso de un microprocesador ESP32 aprovechando que este ya tiene integrada la función y el módulo correspondiente. Es necesario al principio del código agregar las biblotecas de la comunicación y se utilizan los pines RX2 y TX2 para realizar la comunicación de la FPGA al ESP32. 

El código se basa principalmente en realizar la lectura por el puerto serial y enviarlo por el puerto bluetooth. Se imprimen algunos mensajes en pantalla para indicar el correcto funcionamiento del dispositivo y para inicializar la conexión con el celular. [Código en Arduino](/Arduino/Bluetooth/Bluetooth.ino).

```

void loop() {
  if (Serial2.available()) { //Encuentra algo en el Rx
   dato = Serial.read();     //Guarda el dato disponible en el Puerto serial
   SerialBT.write(dato);    //Manda el dato por Bluetooh
   Serial.print(dato);     //Muestra el dato en el Serial del ESP32
  }
}
```
