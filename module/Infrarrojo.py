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
