## Sensor SHT31
El sensor de temperatura debe ser leído con un protocolo I2C. Para ello, se utilizan los puertos SDA y SCL del arduino mega con las diferentes librerías que existen para este propósito. Principalmente, se trabaja con la lubrería Adafruit_SHT31.h pues tiene funciones definidas para leer la temperatura y la humedad a través del protocolo mencionado y se imprimen fácilmente en los puertos seriales. Se inicializan los seriales 0 y 1, para obtener los resultados en consola y transmmitirlos por TX1. Se tienen también algunos mensajes en consola que permiten identificar si el sensor está correctamente conectado y si es posible leer los datos. 

``` clike
void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);

  while (!Serial)
    delay(10);     

  Serial.println("SHT31 test");
  if (! sht31.begin(0x44)) {   // Set to 0x45 for alternate i2c addr
    Serial.println("Couldn't find SHT31");
    while (1) delay(1);
  }

  Serial.print("Heater Enabled State: ");
  if (sht31.isHeaterEnabled())
    Serial.println("ENABLED");
  else
    Serial.println("DISABLED");
}


void loop() {
  float t = sht31.readTemperature();
  float h = sht31.readHumidity();

  if (! isnan(t)) {  
    Serial1.write(t);
  } else { 
    Serial.println("Failed to read temperature");
  }
  
  if (! isnan(h)) {  
    Serial1.write(h);
  } else { 
    Serial.println("Failed to read humidity");
  }

  delay(1000);
}
```
