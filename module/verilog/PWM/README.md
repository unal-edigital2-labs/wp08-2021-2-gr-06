Para implementar el módulo en verilog de los pulsos PWM encargados de girar el servomotor, se implementó el siguiente código principal:
``` verilog
`timescale 1ns / 1ps

module BloquePWM(  
                    output	wire pwm,
                    input	wire [2:0] orden,
		     input	wire clk  
    );
    
   MaquinaEstadosPWM MaquinaEstadosPWM1 (
    .orden (orden),
    .clk(clk),
    .ENABLE (ENABLE),
    .reset (reset),
    .grados (grados)
   );
   
   DivFreqPWM DivisorF   (
                                  .clkin      ( clk     ),
                                  .clkout  ( clkout )
                                );
   PWM pwm1 (
          .clkpwm (clkout),
          .ENABLE (ENABLE),
          .reset (reset),
          .grados (orden),
          .pwm(pwm)
          );
endmodule

```
Este bloque llama a los módulos "MáquinaEstadosPWM", "DivFreqPWM" y "PWM". El primero de ellos se muestra a continuación:

``` verilog 
`timescale 1ns / 1ps

module  MaquinaEstadosPWM  (
                            input clk,
                            input	[2:0] orden,
                            output	reg	ENABLE,
                            output	reg	reset,
                            output  reg [1:0] grados
                          );
	always@(posedge clk)
	begin
	case(orden[2])
		1'b1:	
		begin
			ENABLE <=  1;
	      	reset  <=  0;
		end
		1'b0:
		begin
			reset  <=  1;
	     		ENABLE <=  0;
		end
		default:
		begin
			reset  <=  0;
	     		ENABLE <=  0;
		end
	endcase
	
		case({orden[1],orden[0]})
		2'b00:	
		begin
			grados <=  0; //00 van a ser 0grados
	      	
		end
		2'b01:
		begin
			grados <=  1;  //01 van a ser 90grados
		end
		
		2'b10:
		begin

			grados <=  2;  //10 van a ser -90grados
		end
		
		default:
		begin 	

			grados<=  2'b00;   //11 va a ser un indicador de error
		end
	endcase
	
	end
endmodule
```
Principalmente, el código se encarga de verificar si "enable" está en 1 para empezar a generar el pulso o si el "reset" está activado para borrar todos los datos que se tengan en el momento. Por otro lado, este código también se encarga de leer la variable "orden", la cual indica el ángulo de giro del servo motor para generar el pwm adecuado. Como se ve en el bloque principal, la salida de este módulo serán los grados que el bloque PWM interpretará y generará la el cíclo útil correspondiente.

Se tiene también un divisor de frecuencias, puesto que se necesita un periodo de la señal de 20ms se hace la división del reloj de 100MHz de la FPGA. En el último bloque, se genera la señal mencionada, teniendo encuenta que para obtener una posición de 0° se necesita un ciclo útil de 1.5ms, para un giro de 90° se necesita uno de 2ms y finalmente para un giro de -90° se necesita uno de 1ms.


``` verilog
`timescale 1ns / 1ps

module PWM#(
parameter top=400)  //20ms con el clk
( 
  output reg pwm=0,
  input  [1:0] grados, 
  input ENABLE,
  input reset,
  input clkpwm
    );
reg [10:0] contador;
reg [7:0] ancho;
initial
begin
contador=0;
ancho=30;
end
	always@(posedge clkpwm)
    begin 
      
    if(reset==1)begin 
    contador=0; end
    
 if(ENABLE==1)
  begin  
        contador<=contador+1;
    
  
        if(grados==2'b00) begin
         ancho<=30; end               //numero de ciclos de reloj para hacer 1.5ms
        else if(grados==2'b01) begin
         ancho<=50; end                //numero de ciclos de reloj para hacer 2ms
        else if(grados==2'b10) begin
         ancho<=10; end                //numero de ciclos de reloj para hacer 1ms
        else begin
         ancho<=30; end 
         
        //Creación del pulso modulado      
        if(contador<ancho) begin 
        pwm<=1; end
        else if(contador>=ancho) begin
        pwm<=0; end 
        else  begin
        pwm<=0; end
    
        if(contador>=top-1)begin 
        contador<=0; end
                                                       
  end  
    
end    
endmodule
```

Finalmente se agregan los módulos y los pines el en buildSoCProject.py
``` python
#PWM
SoCCore.add_csr(self,"pwm_cntrl")
self.submodules.pwm_cntrl = pwm.PWM(platform.request("pwm_out"))
```
# Mapa de Memoria - Registros del Periférico
| csr_register| Direccion |      |
| ------------- | ------------- | ------------- |
|pwm_cntrl_orden|0x82007000|rw|
