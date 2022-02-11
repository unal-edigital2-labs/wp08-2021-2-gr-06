Para el módulo de los infrarrojos, se implementó un código sencillo en el que únicamente se asigna la entrada a un registro de salida. El sensor infrarrojos envía un 1 si no detecta ningún fragmento de línea negra, y envía un 0 si detecta la línea. Teniendo en cuenta esto, se realiza el procesamiento de la señal por medio de software y solo se adquiere la señal por medio del hardward.

``` verilog
`timescale 1ns / 1ps

      module Infrarrojo(
      input [4:0] input_infra,
      output [4:0] output_infra
    );

     assign output_infra = input_infra;

    endmodule
```

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
