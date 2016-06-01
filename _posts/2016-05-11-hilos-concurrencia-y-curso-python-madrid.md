---
title: Hilos, concurrencia y Python avanzado
layout: post
---

# Un poco de publi : Curso presencial de Python en Madrid, con Securizame :)
Gracias a Securizame, y junto a 4 compañeros, impartiremos un **curso completo de Python**. Desde la introducción a Python, parte específica para pentesters o sysadmin, hasta la **parte más avanzada (que es la que impartiré yo).**

El índice del curso completo lo podéis consultar en la web de Securizame:

[https://www.securizame.com/nuevos-cursos-online-y-presenciales-en-securizame-python-para-sysadmins-y-pentesters/](https://www.securizame.com/nuevos-cursos-online-y-presenciales-en-securizame-python-para-sysadmins-y-pentesters/)

Para los que os queráis introducir en el mundo de Python, seguro que nos os vendría nada mal alguien que os echara una mano y os guiará en el aprendizaje, verdad? :)

Os recomiendo que le echéis un ojo al índice. Una vez que lo veáis... No tendré que deciros nada más. **Os convenceréis sol@s** :)

# Curso de Python avanzado 
Como os comentaba, la parte que me toca va a ser la parte más avanzada. En que va a consistir? Principalmente se va a centrar en 3 puntos:

-  Estructuración y gestión eficiente de proyectos.
-  Mejora e incremento de rendimiento
-  Concurrencia y distribución de carga
-  Despliegue de proyectos y uso de Docker con Python

Podéis ver el índice completo y ampliado en:

[https://cursos.securizame.com/python-avanzado/](https://cursos.securizame.com/python-avanzado/)

# Para muestra un botón 

Para abrir boca, os voy a contar un mínimo adelanto de lo que veremos en el curso:

## Python y su inexistente paralelismo

Supongo que todos sabéis que son los hilos, verdad? Es un concepto multi-lenguaje de programación. Python, como no podía ser menos también **nos permite usar hilos... O no?**

**Pero... Cómo que NO, si Python tiene la librería threading que nos permite crear hilos?**

Efectivamente, la librería existe. Pero, es una de las grandes "mentirijillas" de Python :) 

## Por qué Python nos "miente", qué le he hecho yo? 

A modo de culturilla: 

Cuando Guido van Rossum (creador de Python) ideó y diseño Python, tenía muy clara una cosa: tenía que ser muy simple. **No solo el lenguaje, también el intérprete**.

Con esta idea en la cabeza, creó el intérprete sin soporte para hilos.  Pero, con los años, los años los programadores reclamaban más y más el soporte de hilos.

Pero claro, la inclusión de hilos suponía complicar el intérprete. Y mucho. Pero... por qué? Porque el paralelismo tiene, ente otros muchos problemas a solucionar:
-  Sincronización 
-  Condiciones de carrera 
-  Interbloqueos
-  Fugas de memoria

## Python y los falsos "hilos"
Pese a todo, los programadores seguían reclamando hilos. Así que lo solucionaron de la siguiente manera:
-  Crearon el **GIL (Global Python Interpreter)**.
-  Crearon una librería que permitía al programador usar un API para la creación y gestión hilos.

Vale... y es esto qué es? :)

## El GIL

Como ya hemos comentado, la inclusión de hilos supone mucho esfuerzo y complicación del intérprete. El GIL lo que hace es **SIMULAR** la ejecución de hilos. Es decir:

- Python crea 1 proceso y 1 hilo por defecto. Cualquier programa que hagamos, se ejecutará en este contexto.
- **Si creamos más hilos** Python y el GIL lo que harán será ir cambiando la ejecución de cada hilo en el procesador. De tal manera que **SOLO se ejecuta un hilo a la vez**.  Es decir, que **lograremos concurrencia** pero **NO paralelismo**, como nos dice la intuición. 

Vaya KK, verdad? :) la verdad es que cuando te enteras de esto la primera vez, te quedas bastante decepcionado. Al menos yo me quedé pensando: pero qué tipo de lenguaje de mi***da es este?!?!:)

Tened cuenta lo que os comentaba más arriba: Python fue creado para ser simple. En todos los aspectos. Esto no tiene que ser necesariamente malo, **todo depende de lo que necesitemos**. Por ejemplo, no se me ocurrirá escribir un sistema operativo o sistema el control de un misil en Python :)

A pesar del GIL, en general, con Python podremos hacer la mayor parte de cosas que se nos pasen por la cabeza, no preocuparse :)

## Sobreviviendo al GIL
Vale, ya sabemos que Python no tiene hilos reales. Entonces, cómo podemos hacer si necesitamos incrementar el rendimiento? Bueno, pues tenemos muchas soluciones:
- **Mulitprocesing**
- Hilos ligeros
- **Corrutinas**
- **Procesamiento distribuido** 
- Uso de técnicas JIT (Just In Time)
- **Compilación de de todo o parte de nuestro código Python**
- **Uso de otros intérpretes de Python "no oficiales"**
- Uso de C para partes críticas con wrapper en Python.
- Transformación de entrada/salida orientada a eventos.
- etc...

Como veis, opciones hay :) Todo depende del tipo problema que necesitemos abordar: uso intenso de red, carga de cómputo... 

**En el curso estudiaremos los puntos marcados en negrita**. Sí, intenso. Pero nos os preocupéis, que explicado no es tan difícil :)

La aproximación más fácil, sin duda (sobre todo a nivel de compresión del concepto) es la primera opción: **multiprocesing**:

Esta aproximación es tan sencilla como que, en lugar de crear hilos, crearemos procesos. Así de fácil. Los procesos de ejecutarán en cores diferentes del procesador, con lo que conseguiremos paralelismo real.

**OJO** que esto no es panacea, y tiene muchos problemas y no puede ser usado para todo. **No os preocupéis que veremos sus pros y contras**.

## Por último: Un curioso caso
Como ya sabemos, los hilos en Python no existen como los entendemos en otros lenguajes. Esto da lugar a cosas curiosas, como las que os voy a contar: **Cuando la ejecución con hilos es más lenta que la ejecución SIN hilos**

Tomemos el siguiente ejemplo: un productor que genera números del 1 a 1.000.000, y un/os consumidores que operan con esos números generados.

El código del caso SIN hilos:

	def countdown(n):   
	    while n > 0:
	        n -= 1

	def main():
	    countdown(100000000)

	if __name__ == '__main__':
	    main()


El código del caso CON hilos. Permitimos la ejecución de 20 hilos en paralelo:

	from threading import Thread

	def countdown(n):
	    while n > 0:
	        n -= 1

	def main():

	    COUNT = 100000000

	    t1 = Thread(target=countdown, args=(COUNT//4, ))
	    t2 = Thread(target=countdown, args=(COUNT//4, ))
	    t3 = Thread(target=countdown, args=(COUNT//4, ))
	    t4 = Thread(target=countdown, args=(COUNT//4, ))

	    t1.start(); t2.start(); t3.start(); t4.start()

	    t1.join(); t2.join(); t3.join(); t4.join()

	if __name__ == '__main__':
	    main()

Si ejecutamos cada uno de los códigos, obtenemos los siguientes resultados de ejecución:

	# python count.py
	real    0m6.820s
	user    0m6.585s
	sys     0m0.079s

	# python threads-count.py 
	real    0m15.583s
	user    0m10.851s
	sys     0m14.071s

Ostras! la ejecución **SIN hilos has sido más rápida!**. Pero... Por qué? Sin entrar en mucho detalles (lo dejo para posteriores POST), lo que ha ocurrido es lo siguiente:

1. Como ya sabemos, Python simula la concurrencia, 
2. Python intercambia la ejecución de los hilos para que solo se ejecute 1 a la vez,
3. Este cambio de contexto, en determinadas situaciones, es más costoso que el trabajo en si que va a realzar el propio hilo. 
4. Por lo tanto: **la solución mono-hilo es más rápida porque no gasta tiempo en los cambios de contexto y porque el trabajo a realizar por cada hilo es menos costos que el cambio de contexto**

Para los expertos de Python que leáis esto: se que me dejó muchos detalles y que es una explicación muy simplificada :)

# Conclusión 
El mundo de la concurrencia y paralelismo, en cualquier lenguaje de programación, es complicado aunque muy interesante. En Python, además, puede llegar a ser un reto :)

En el siguiente POST os contaré más cosillas del mundo oscuro de la concurrencia en Python.

**Nos vemos en Junio en Securizame!**
