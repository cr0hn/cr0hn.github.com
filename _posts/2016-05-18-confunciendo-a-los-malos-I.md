---
title: Confundiendo a los malos (I)
layout: post
---

Siguiendo con mi recien adquirida costumbre de escribir un POST a la semana en el mentro de camino al curro, vamos a seguir con otro tema curioso: **Cómo engañar a los malos** 

# De qué va este Post?

Hoy la vamos a ver cómo **cambiando 3 líneas** de nuestro **servidor web** podemos **confundir a un atacante**.

# Por qué puedo querer confundir a un atacante?

Bueno, tal vez estéis muy orgullos de vuestro Apache, Tomcat, Nginx o cualquier otro, pero... No deja de ser un software. Y por definición, el software puede tener fallos. 
A pesar, incluso, de tener parcheado y bien configurado vuestro servidor, **es imposible conocer todos los ataques, y más aquellos que no son públicos** y que a los que podríamos ser vulnerables.

Ante esta situación no podemos hacer nada, tan solo tratar de mitigar o prevenir. Por eso, **os propongo una idea algo diferente**

**Engañemos a aquellos que nos traten de atacar**.

# Cómo engañamos a un atacante?

Existen muchísimas formas de hacerlo, pero hoy vamos a ver solo una pincelada. Nuestro objetivo es es el siguiente:
Cuando una atacante se conecte a nuestro servidor web, **le haremos pensar que es un servidor diferente al que realmente tenemos instalado**

Es decir: cambiaremos el banner de nuestro servidor web por otro.
Qué tonto verdad? Sí, lo es, pero veréis que efectivo resulta.

# Cómo lo hacemos?

En el caso que nos aplica lo vamos a ver con el **servidor web Nginx**, por ser mi preferido, pero podéis trasladar el concepto a cualquier otro. Manos a la obra!

En primer lugar instalamos el paquete *nginx-extras*:

    # sudo apt-get install nginx-extras

Añadimos al fichero de configuración del nginx lo siguiente:

    # vim /etc/nginx/nginx.conf
    
    http {
        ...    
        server_tokens off;
        server_name_in_redirect off;
        more_set_headers 'Server: Microsoft-IIS/8.5';
        ...


# Qué hemos hecho?

He hemos dicho al servidor web que nos sustituya la cabecera HTTP que devuelve al usuario, por la que le hemos indicado.

Ahora un matiz **muy importante: que valor deberíamos de poner ahí**?

No hay nada exacto, pero mi recomendación es que si queréis engañar a un "malo" creéis una mentira plausible. Es decir: que cuando éste analice vuestro servidor, la mentira sea creíble. 

Y **cómo la hacemos creíble?**. Fácil! 

Probablemente cualquier atacante lo primero que use para identificar nuestros sistemas sea el *nmap*, verdad? Luego, si logramos engañar a nmap, es bastante probable que engañemos al "malo". 

# Cómo nos identifica nmap?

Contrariamente a lo que pueda parecer, es **muy fácil engañar al nmap**.

Si bien es cierto que la parte de red es algo más compleja, no es así en la identificación de los servicios que hay abiertos detrás de cada puerto, donde la identificación la hace, en su mayoría, con unos simple REGEX (expresiones regulares). 

Nmap tiene una base de datos con dichas expresiones. Lo único que tendremos que hacer será que nuestro banner haga válida una de dichas expresiones en el puerto 80 o 443, verdad? A que ahora parece más fácil? :)

Si os fijáis bien, el banner que elegí arriba coincide con una de las expresiones de la base de datos del nmap:
 
    (5070) match http m|^HTTP/1\.1 400 .*\r\nServer: Microsoft-IIS/(\d[-.\w]+)\r\n| p/Microso      ft IIS httpd/ v/$1/ o/Windows/ cpe:/a:microsoft:iis:$1/ cpe:/o:microsoft:windows/a 

En la versión 7.01 del Nmap, esta expresión está en la linea 5070.

Podéis encontrar el fichero en:

MAC:
    
    /opt/local/share/nmap/nmap-service-probes

Kali Linux:

    /opt/share/nmap/nmap-service-probes
    
   
# Demostración 

No se vosotros, pero yo no me creo nada que no pueda comprobar :) y, en este caso, comprobarlo es muy sencillo. Un simple nmap al puerto de nuestro server y...

![nmap](/examples/confundiendo-a-los-malos-i/nmap.jpg)

# Conclusiones

Como ultimas palabras comentar varias cosas:

* Este tipo de técnicas se llaman **técnicas anti-fingerprinting**. 
* Aunque en este ejemplo hemos usado nmap, os invito a que uséis Nessus, OpenVas o similares. Veréis como las pruebas las orienta al servidor que habéis indicado, por lo que las prueba no obtendrán resultados coherentes.

Os iré contando más técnicas sencillas de anti-fingerprinting. Veréis como **no es tan complicado engañar a los malos** :)

Chau!
