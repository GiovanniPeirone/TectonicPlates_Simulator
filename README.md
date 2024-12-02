# Lo Mas Sercano

Prueba 7

Prueba 8

# Prompt

Hola chat.
Quiero crear un simulador choque de placas tectónicas para hacerlo necesito que uses python y pygame.
Para comenzar necesito que crees un grid enorme  con una cantidad de filas y columnas semejante al doble del tamaño de la pantalla. Ahora en cada posición del grid lo que vamos a hacer es dibujar un color el cual va a representar una altura.
En base a esto necesito que generes algo que represente un terreno el cual tiene que tener montañas y zonas bajas esto se va a representar de esta manera 

Altura 0 - color base es para la altura del mar osea que quiero color celeste
Altura 1 - Este va a ser amarillo y representa la playas
Altura 2 - Este color debe ser verde claro y representa las zonas más llanas
altura 3  a 15 	- Estas alturas se va a ir oscureciendo según qué tan alta es la altura osea que 15 seria casi negro total y 3 casi el mismo color que el de la altura 2  y tambien quiero que el color verde valla convirtiéndose enun marron

Aqui hay un ejemplo sobre cómo podría ser el mapeo del terreno
en el que hay filas y columnas

000000000000111111111001100000000000000000000000000
00001111111111222221111211111111111100000000000000000
00000122222222222222222222222211111110000000000000
00000122233355555666665555666655443321110000000000
00000122233333333445555554445544434331100000000000
00000012233333344444444433333441110000000000000000
00000001222332223333333333333110000000000000000000
00000000111222222222222222222100000000000000000000
0000000000011111111111111111110000000000000000000000

Esto los puedes generar con ruido de perlin

Luego tendrias que por pantalla tomar la lista de valores y pintar por pantalla los colores según la altura.


Muy bien pero hasta ahora no tenemos nada que ver con placas tectónicas por lo que necesito que una vez el terreno esté generado dividas la pantalla en una con una línea blanca con forma uniforme. entonces ahora el lado izquierdo de la pantalla es una placa tectónica y el derecho es otra ejemplo 


000000000000111111111000000!0000000000000000000000000000
0000111111111122222111000001!00011111111100000000000000000
00000122222222222222200000!00222222211111110000000000000
00000122233355555666600000!05555666655443321110000000000
0000012223333333344550000!00554445544434331100000000000
00000012233333344444400000!00033333441110000000000000000
00000001222332223333000000!033333333110000000000000000000
0000000011122222222000000!22222222100000000000000000000
000000000001111100000!0000111111110000000000000000000000


y luego de manera aleatoria el terreno de una de las placas tectónicas se va a empezar a dirigir hacia la otra ejemplo el terreno de el de la izquierda se queda quieto y el de la derecha se mueve hacia la izquierda. ahora para simular que una la que se está moviendo hacia la izquierda se está metiendo por debajo de la placa tectónica que está quieta cuando el terreno de la derecha pase la línea hacia la izquierda va a desaparecer.
Pero el terreno de arriba debe ser modificado por el de abajo por lo que si la altura en la placa de abajo es 3 y en la placa de arriba es 5 se suman y muestra un nuevo color de número 8

Una vez ya no quede más terreno visible de la parte de abajo el programa termina pasando y dejando la imagen final del terreno.


Adicional:

Si apreto espacio se reinicia la simulación
El preogrma te deve dejar ver la simulacion en tiempo real

