---
title: Ocultando información en sitios curiosos - I
layout: post
---

# Ocultando información en sitios curiosos (I)

Tras mucho tiempo me he propuesto tratar de coger la costumbre de escribir alguna entrada de forma regular. Contando mis locuras e investigaciones, dadas por la falta de sueño :)

Así que... A empezar!

# De qué va este post?

En esta serie de post hablaré de lugares extraños y, sobre todo, curiosos donde esconder información:

# Hoy: ocultando información en boolean.io

El otro día, gracias a mis compañeros de trabajo, descubrí el siguiente servicio:

[Boolean.io](http://boolean.io)

**De qué va esto?**

Pues es un tanto peculiar, ya lo que ofrecen es "booleanos como servicio". Curioso, no?

**Qué es eso de boolean as a service?**

Lo que ellos llaman *"boolean as a service"* no es ni más ni menos que te dejen guardar un "true" o un "false" y te den una URL única asociada. Es decir:

Si quiérenos guardar un "true", nos podrían dar la siguiente URL:

http://boolean.io/heouwjfyosllndhw7gh628jdjf/

Cada vez que la consultemos, se nos devolverá un "true", serializado en JSON.

Ademas, nos dan la posibilidad de cambiar el true a un false, siempre y cuando sepamos el ID que el sitio nos ha proporcionado.

**Cabe destacar que el acceso no es autenticado**.

# Todo son ceros y unos

Como bien sabemos, todo software, al final acabará convirtiéndose en un "0" (false) o un "1" (true), cierto?

Y si cogiéramos un mensaje, los descompusiéramos en cada uno de sus caracteres y cada carácter lo convirtiéramos en su correspondiente valor binario? Y si cogiesemos esa cadena binaria y la guardaremos, valor a valor, en boolean.io?

Pues lo que pasaría es que boolean.io nos daría un identificador por cada valor guardado. Tan solo tendíamos que guardar ese ID y el orden en el que insertamos la información. 

Para recuperar esa información tendríamos que hacer el proceso contrario: coger cada ID, en orden, e ir recuperando valor a valor, hasta formar el mensaje oculto inicial.

Un poco enrevesado? Puede, pero ya se sabe, cuando el diablo se aburre... :)

# Let's go!

Tras la teoría, veamos si es posible ocultar informacion realmente como os he contado:

El día que mis compañeros me comentaron esto, tardamos poco en comer, así que me puse 10 minutillos y me hice un pequeño script. Lo podeís encontrar **-->** [aquí](https://github.com/cr0hn/bo) **<--**

Está hecho en Python, y es muy fácil de utilizar:

**Instalación**

	pip install -r requirements.txt
	
**Generando la información a ocultar**

Hay que tener en cuenta que **la cantidad de información que podemos oculta es bastante pequeña**, además, el servicio está limitado a 40 peticiones por minuto.

Así que vamos a hacer una prueba con las letras "a\n". Es decir: la letra "a" y un salto de carro. 

Creamos el fichero con la información:

	echo "a" > info_to_hide.txt
	
**Uso - Ocultando información**

Ahora ya solo nos queda ejecutar el script de ocultación:

	# python hide.py -f info_to_hide.txt -o hidden.db
	[i] Storing char: 'a'
	    |- Storing bit '0'
    	|- Storing bit '1'
	    |- Storing bit '1'
	    |- Storing bit '0'
	    |- Storing bit '0'
    	|- Storing bit '0'
	    |- Storing bit '0'
    	|- Storing bit '1'
	[i] Storing char: '
	'
	    |- Storing bit '0'
    	|- Storing bit '0'
	    |- Storing bit '0'
    	|- Storing bit '0'
	    |- Storing bit '1'
    	|- Storing bit '0'
	    |- Storing bit '1'
    	|- Storing bit '0'
	
El fichero generado *hidden.db* es el que contiene las referencias y orden que nos ha devuelto el server, tal y como comenté arriba, recuerdas? Si lo abrís es un fichero JSON muy sencillo.

**Uso - Recuperando información oculta**

Con el fichero *hidden.db* podemos recuperar los datos ocultados (nosotros o cualquier que lo tenga!):

	# python unhide.py -f hidden.db
	[i] Starting ...
	    |- Reading: 'dc342f87-39dd-4f97-8188-32ab312bc0a8'
    	|- Reading: '60375eb1-7f02-4398-a8b7-a2ea1eedccd8'
	    |- Reading: 'aa0aada9-5ae5-46a3-b2f9-de269ebc986b'
	    |- Reading: '4311b005-e958-422d-bb4c-f625d23924ca'
    	|- Reading: 'd254560a-5351-4a48-a2c0-008faa1b1a9a'
	    |- Reading: '6a31180e-1394-4b70-a305-599beb5114da'
    	|- Reading: '7523af15-e7c8-45a4-81e6-f989570dac0d'
	    |- Reading: 'b1fbdcfc-531c-47d5-9d9c-b97ab26927a5'
    	|- Reading: 'a3f8f3a9-cab5-4e84-b83a-b5c758085f49'
	    |- Reading: '13910781-907c-43c9-9fcd-66e255380628'
    	|- Reading: '4606d74c-4b46-42f5-8ebc-846e5680b816'
	    |- Reading: '80c13529-818e-4761-91c6-55dd0d427935'
    	|- Reading: '2a02bcd0-0458-4d4f-b50c-c5a5d6647965'
	    |- Reading: 'e81021ce-cd73-42dc-ae55-e520a5fd9fc7'
    	|- Reading: '1dd260fc-7ad6-4046-b5ab-4386cce9957f'
	    |- Reading: 'fc8d3490-a189-4ae9-9d29-dee8da2fe56d'
	
	[i] Hidden message: 'a
	'	

E voilà! Información recuperada!

# Conclusión

Sí, se que este ejemplo es muy tonto, pero no me negaréis que es curioso :)

Os veo en mi siguiente ocurrencia escrita.

Chau!




