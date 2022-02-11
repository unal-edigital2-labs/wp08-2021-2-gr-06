# ULTRASONIDO

El ultrasonido realiza el mapeo del laberinto y detecta los obstaculos o paredes. El ultrasonido recibe un pulso por el trigger, iniciando la emision de la onda y empieza un conteo en el modulo hasta que se recibe una onda similar a la enviada por el ECHO. Dado que la onda va hasta el objeto y rebota, el tiempo que se mide es el doble del que se debe tener para el cálculo de la distancia. Puesto que se envia una onda sonora y conocemos la velocidad del sonido, podemos realizar el calculo de la distancia: 

Distancia=Tiempo*342/2

```verilog

module	divisorfrec	#(
				parameter top=12'b101101101100
			)
			(
				input           clk,
				output	reg	CLKOUT
			);

	reg [11:0] count_2924;
	
	initial
	begin
		CLKOUT=1'b1;
		count_2924=0;
	end
	
	always @(posedge clk) 
	begin
		count_2924 <= count_2924 + 1;
		if(count_2924 == top)
		begin
			count_2924<=0;
			CLKOUT <= ~CLKOUT;
		end
	end
endmodule

```

Con el nuevo reloj del sistema, se sabe que será necesario un contador para registrar el tiempo que pasa entre la salidad de la señal y su llegada. Para ello se hace uso de la siguiente funcion If-else la cual indicara cuando debe empezar a contar el reloj.

``` verilog
if(reset)
		begin
			count0=0;
			calculate=0;
			pulse=0;
		end

		else
		begin
			if(ENABLE)
			begin
				pulse=1'b1;
			end
			
			if(ECHO)
			begin
				count0=count0+1;
			end
			
		end
	end

```

Dado que ya se tiene la informacion del tiempo que demora la señal en ir hasta el objeto y regresar, se calcula la distancia. Con el objeto ultrasonido.py, se asignan las variables trigger y echo a pines físicos, la variable orden a un registro de escritura y las variables done y distancia a registros de lectura.

``` python

class Ultrasonido(Module,AutoCSR):
    def __init__(self, trigger, echo):
        self.clk = ClockSignal()   
        self.rst = ResetSignal()

        self.trigger = trigger
        self.echo = echo

        self.orden = CSRStorage(1)
        self.done = CSRStatus(1)
        self.distancia = CSRStatus(8)

 self.specials +=Instance("bloqueultrasonido",
            i_clk = self.clk,
            i_rst = self.rst,
            i_orden = self.orden.storage,
            i_echo = self.echo,
            o_trigger = self.trigger,
            o_done = self.done.status,
            o_d = self.d.status,
        )

```


Se agrega este modulo en el buildSocproject.py donde se asignaran las variables de entrada y salida, y tambien se crean los registros para que se pueda hacer uso de este dispositivo:

``` python
 
 SoCCore.add_csr(self, "ultrasonido")
self.submodules.ultrasonido = ultrasonido.Ultrasonido(platform.request("us_trigger"), platform.request("us_echo"))

```
