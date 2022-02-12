# Módulos
Se presenta toda la información de los módulos, tanto los archivos de Python como los de Verilog. En cuanto al funcionamiento de estos módulos, puede hacer click en los siguientes enlaces. 
- [IR](/module/verilog/Infrarrojo)
- [Motor](/Motor.md) 
- [PWM](/module/verilog/PWM)
- [Ultrasonido](/module/verilog/Ultrasonido)

## Uart
Para la implementación del protocolo UART, se hizo uso de los archivos de litex creados para este propósito. Para poder utilizar el protocolo es necesario agregar las siguientes líneas de código en el archivo [builSoCProject.py](/buildSoCProject.py):

```python
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
```
Y asignar los pines RX1 y TX1 en el archivo [nexys4ddr.py](/nexys4ddr.py):
```python
("uart1", 0,
    Subsignal("tx", Pins("H4")),
    Subsignal("rx", Pins("H1")),
    IOStandard("LVCMOS33"),
)
```
Este proceso se puede repetir para implementar más pines con estos protocolos de comunicación, únicamente se debe tener en cuenta que se cambia "uart1" por "uart2", y así para tantos protocolos se quieran instanciar.

Se obtuvieron las siguientes direcciones de memoria para cada uno de los registros de los protocolos UART utilizados durante la prueba del robot. 
| csr_base| Direccion |    |
| ------------- | ------------- | ------------- |
|uart1_rxtx|0x82004000|rw|
|uart1_txfull|0x82004004|ro|
|uart1_rxempty|0x82004008|ro|
|uart1_ev_status|0x8200400c|ro|
|uart1_ev_pending|0x82004010|rw|
|uart1_ev_enable|0x82004014|rw|
|uart1_txempty|0x82004018|ro|
|uart1_rxfull|0x8200401c|ro|
|uart2_rxtx|0x82005000|rw|
|uart2_txfull|0x82005004|ro|
|uart2_rxempty|0x82005008|ro|
|uart2_ev_status|0x8200500c|ro|
|uart2_ev_pending|0x82005010|rw|
|uart2_ev_enable|0x82005014|rw|
|uart2_txempty|0x82005018|ro|
|uart2_rxfull|0x8200501c|ro|
|uart3_rxtx|0x82006000|rw|
|uart3_txfull|0x82006004|ro|
|uart3_rxempty|0x82006008|ro|
|uart3_ev_status|0x8200600c|ro|
|uart3_ev_pending|0x82006010|rw|
|uart3_ev_enable|0x82006014|rw|
|uart3_txempty|0x82006018|ro|
|uart3_rxfull|0x8200601c|ro|
