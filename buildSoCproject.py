#!/usr/bin/env python3

from migen import *
from migen.genlib.io import CRG
from migen.genlib.cdc import MultiReg

import nexys4ddr as tarjeta
#import c4e6e10 as tarjeta

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.interconnect.csr import *

from litex.soc.integration.soc import *

from litex.soc.cores import gpio
from litex.soc.cores import uart
from module import rgbled
from module import sevensegment
from module import vgacontroller
from module import camara
from module import Infrarrojo
from module import pwm
from module import ultrasonido


# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
	def __init__(self):
		platform = tarjeta.Platform()
		
		## add source verilog

		platform.add_source("module/verilog/camara.v")

		platform.add_source("module/verilog/Infrarrojo/Infrarrojo.v")

		platform.add_source("module/verilog/PWM/BloquePWM.v")
		platform.add_source("module/verilog/PWM/PWM.v")
		platform.add_source("module/verilog/PWM/MaquinaEstadosPWM.v")
		platform.add_source("module/verilog/PWM/DivFreqPWM.v")

		platform.add_source("module/verilog/Ultrasonido/bloqueultrasonido.v")
		platform.add_source("module/verilog/Ultrasonido/contador.v")
		platform.add_source("module/verilog/Ultrasonido/divisor.v")
		platform.add_source("module/verilog/Ultrasonido/divisorfrec.v")
		platform.add_source("module/verilog/Ultrasonido/divisorfrecd.v")
		platform.add_source("module/verilog/Ultrasonido/divisorfrecgen.v")
		platform.add_source("module/verilog/Ultrasonido/divisorfrecme.v")
		platform.add_source("module/verilog/Ultrasonido/genpulsos.v")
		platform.add_source("module/verilog/Ultrasonido/maquinadeestados.v")
		platform.add_source("module/verilog/Ultrasonido/meultrasonido.v")
		platform.add_source("module/verilog/Ultrasonido/ultrasonido.v")
		clk_freq =100e6

		# SoC with CPU
		SoCCore.__init__(self, platform,
 			cpu_type="picorv32",
#			cpu_type="vexriscv",
			clk_freq=100e6,
			integrated_rom_size=0x10000,
			integrated_main_ram_size=16*1024)

		# Clock Reset Generation
		self.submodules.crg = CRG(platform.request("clk"), ~platform.request("cpu_reset"))

		# Leds
		SoCCore.add_csr(self,"leds")
		user_leds = Cat(*[platform.request("led", i) for i in range(10)])
		self.submodules.leds = gpio.GPIOOut(user_leds)
		
		# Switchs
		SoCCore.add_csr(self,"switchs")
		user_switchs = Cat(*[platform.request("sw", i) for i in range(8)])
		self.submodules.switchs = gpio.GPIOIn(user_switchs)
		
		# Buttons
		SoCCore.add_csr(self,"buttons")
		user_buttons = Cat(*[platform.request("btn%c" %c) for c in ['c','r','l']])
		self.submodules.buttons = gpio.GPIOIn(user_buttons)
		
		# 7segments Display
		SoCCore.add_csr(self,"display")
		display_segments = Cat(*[platform.request("display_segment", i) for i in range(8)])
		display_digits = Cat(*[platform.request("display_digit", i) for i in range(8)])
		self.submodules.display = sevensegment.SevenSegment(display_segments,display_digits)

		# RGB leds
		SoCCore.add_csr(self,"ledRGB_1")
		self.submodules.ledRGB_1 = rgbled.RGBLed(platform.request("ledRGB",1))
		
		SoCCore.add_csr(self,"ledRGB_2")
		self.submodules.ledRGB_2 = rgbled.RGBLed(platform.request("ledRGB",2))
		
				
		# VGA
		SoCCore.add_csr(self,"vga_cntrl")
		vga_red = Cat(*[platform.request("vga_red", i) for i in range(4)])
		vga_green = Cat(*[platform.request("vga_green", i) for i in range(4)])
		vga_blue = Cat(*[platform.request("vga_blue", i) for i in range(4)])
		self.submodules.vga_cntrl = vgacontroller.VGAcontroller(platform.request("hsync"),platform.request("vsync"), vga_red, vga_green, vga_blue)
		
		
		# UART 1
		self.submodules.uart1_phy = uart.UARTPHY(
			pads     = platform.request("uart1"),
			clk_freq = self.sys_clk_freq,
			baudrate = 9600)
		self.submodules.uart1 = ResetInserter()(uart.UART(self.uart1_phy,
			tx_fifo_depth = 16,
			rx_fifo_depth = 16))
		self.csr.add("uart1_phy", use_loc_if_exists=True)
		self.csr.add("uart1", use_loc_if_exists=True)
		if hasattr(self.cpu, "interrupt"):
			self.irq.add("uart1", use_loc_if_exists=True)
		else:
			self.add_constant("UART_POLLING")	
			
		# UART_2
		
		self.submodules.uart2_phy = uart.UARTPHY(
			pads     = platform.request("uart2"),
			clk_freq = self.sys_clk_freq,
			baudrate = 9600)
		self.submodules.uart2 = ResetInserter()(uart.UART(self.uart2_phy,
			tx_fifo_depth = 16,
			rx_fifo_depth = 16))
		self.csr.add("uart2_phy", use_loc_if_exists=True)
		self.csr.add("uart2", use_loc_if_exists=True)
		if hasattr(self.cpu, "interrupt"):
			self.irq.add("uart2", use_loc_if_exists=True)
		else:
			self.add_constant("UART_POLLING")
			
		#UART_3
		
		self.submodules.uart3_phy = uart.UARTPHY(
			pads     = platform.request("uart3"),
			clk_freq = self.sys_clk_freq,
			baudrate = 9600)
		self.submodules.uart3 = ResetInserter()(uart.UART(self.uart3_phy,
			tx_fifo_depth = 8,
			rx_fifo_depth = 8))
		self.csr.add("uart3_phy", use_loc_if_exists=True)
		self.csr.add("uart3", use_loc_if_exists=True)
		if hasattr(self.cpu, "interrupt"):
			self.irq.add("uart3", use_loc_if_exists=True)
		else:
			self.add_constant("UART_POLLING")

			
			
		#Infrarrojo
		SoCCore.add_csr(self,"infra_cntrl")
		infras_in = Cat(*[platform.request("input_infra", i) for i in range(5)])
		self.submodules.infra_cntrl = Infrarrojo.Infrarrojo(infras_in)
		

		#PWM
		SoCCore.add_csr(self,"pwm_cntrl")
		self.submodules.pwm_cntrl = pwm.PWM(platform.request("pwm_out"))

		#Ultrasonido
		SoCCore.add_csr(self, "ultrasonido")
		self.submodules.ultrasonido = ultrasonido.Ultrasonido(platform.request("us_trigger"), platform.request("us_echo"))

	

# Build --------------------------------------------------------------------------------------------


if __name__ == "__main__":
	builder = Builder(BaseSoC(),csr_csv="Soc_MemoryMap.csv")
	builder.build()

