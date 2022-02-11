## Infrarrojo
Para la implementación del módulo de verilog se realizó una implementación sencilla que únicamente asigna la entrada del sensor a un registro de salida. Si alguno de los sensores detecta un fragmento de la línea negra se envía un 0, mientras que si no detecta nada envía un 1. Es importante tener en cuenta esto para realizar posteriormente el análisis y procesamiento de datos por medio de software. El hardware solamente se encargará de recoger la información enviada por el sensor.
``` verilog
`timescale 1ns / 1ps

module Infrarrojo(
input [4:0] input_infra,
output [4:0] output_infra
);

assign output_infra = input_infra;

endmodule
```

En cuanto a el código en python, se asignan los pines "input_infra" a conexiones físicas de la tarjeta. Por otro lado se declara un registro de lectura de 5 posiciones encargado de almacenar la información de los sensores infrarrojos.

``` python    
from migen import *
from migen.genlib.cdc import MultiReg
from litex.soc.interconnect.csr import *
from litex.soc.interconnect.csr_eventmanager import *

# Modulo Principal
class Infrarrojo(Module,AutoCSR):
def __init__(self, input_infra):

self.input_infra = input_infra
self.output_infra = CSRStatus(5)

self.specials +=Instance("Infrarrojo",
    i_input_infra = self.input_infra,
    o_output_infra = self.output_infra.status,
)
```
Se agregan los pines y los módulos en el buildSoCProjetc.py
``` python
#Ultrasonido
SoCCore.add_csr(self, "ultrasonido")
self.submodules.ultrasonido = ultrasonido.Ultrasonido(platform.request("us_trigger"), platform.request("us_echo"))
```
