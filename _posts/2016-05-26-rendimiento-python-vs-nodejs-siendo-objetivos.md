---
title: "Rendimiento: Python vs NodeJS - Tratando de hacer una comparativa justa (I)"
layout: post
---

Y aquí sigo una semana más dando guerra. Hoy vamos a ver un tema que seguro que generará diversidad de opiniones: **Python vs NoseJS** :)

Antes de nada decir que, a pesar de ser programador Python y de que no soy un fan de NodeJS, **trataré ser objetivo**. Si las los test que salgan dicen que NodeJS proporciona un mejor rendimiento, **lo asumiré como un hombre y seguiré con mi vida.** XD

Antes de dar paso al POST, **recordaros que, Comenzamos esta semana con los cursos de Python en Securízame (en Madrid). Desde cero hasta a avanzado (la parte avanzada corre a mi cargo)**. Toda la info aquí: https://cursos.securizame.com/python-avanzado/

# De qué va este POST?

En este POST haré diferentes pruebas de carga y rendimiento a fin de ver que lenguaje de programación nos da más potencia para el desarrollo web. Siempre desde el punto de vista del rendimiento.

No voy a entrar en cuestiones como sencillez de programación, paradigmas usados o cualquier otra cuestión ya que muchas de ellas son muy subjetividad, y no es el objetivo.

# Qué compararemos?

En las pruebas, vamos a testear:

- **NodeJS**, con el módulo **Express**.
- **Python** con **asyncio**, y con el módulo **aiohttp**.

Con Python veis que usaremos asyncio y aiohttp, y con NodeJS no usaremos ningún módulo adicional para proporcionar asincronismo. Por qué? Porque **NodeJS está orientado a eventos** y forma **parte de su ADN**, así como la creación de servicios web. 

Python, por otro lado, su funcionamiento normal no está o orientado a eventos. **Para hacer las pruebas de formas más justa**, usaremos el nuevo módulo de Python 3.4 **asyncio**, que nos proporciona esa funcionalidad, y **aiohttp** que nos facilita la creación de servidores HTTP sobre asyncio.

**Nota**: En Python existen más librerías que nos proporcionan asincronía, pero usaremos asyncio por ser la que pretende ser punto de referencia en Python a día de hoy.

# Cómo haremos las pruebas?

Las pruebas serán muy sencillas:

**Sitio testeado**

Un pequeño servidor web con que devuelve una página en HTML.

**Pruebas**

El objetivo es medir:

- Cantidad de peticiones que pueden atender por segundo.
- Tiempo total empleado en procesar X peticiones.
- Cantidad de clientes concurrentes que son capaces de atender.

# código usado

Estos son los fuentes que usaremos para hacer las pruebas:

**Python**

```python

import asyncio

from aiohttp import web


@asyncio.coroutine
def home(request):
    return web.Response(body=b"""<!DOCTYPE html>
<html lang="es">
<head>
  <title>Hello world!</title>
</head>
<body>
<p>P&aactue;gina de prueba</p>
</body>
</html>""")


@asyncio.coroutine
def json_path(request):
    return web.json_response({"test": 1, "data": "hello world" })


def main():
    app = web.Application()
    app.router.add_route('GET', '/', home)
    app.router.add_route('GET', '/json', json_path)

    web.run_app(app, port=8081, backlog=5000)

if __name__ == '__main__':
    main()
```

**NodeJS**

```javascript

const express = require('express');

// Constants
const PORT = 8080;

// App
const app = express();

// End-points
app.get('/', function (req, res) {
  res.send(`<!DOCTYPE html>
<html lang="es">
<head>
  <title>Hello world!</title>
</head>
<body>
<p>Página de prueba</p>
</body>
</html>`);
});


app.get('/json', function (req, res) {
  res.send(JSON.stringify({ test: 1, data: "hello world" }));
});

// Start server
app.listen(PORT, backlog=5000);

console.log('Running on http://localhost:' + PORT);
```

**Nota**: Para hacer las pruebas correctamente tendremos que ajustas las propiedades del kernel de nuestro sistema, a fin de incrementar los valores por defecto y ser capaces de atender más conexiones que las que vienen configuradas. Aquí podéis encontrar los comandos a ejecutar:

http://b.oldhu.com/2012/07/19/increase-tcp-max-connections-on-mac-os-x/

# Resultados

## Tiempo en procesar peticiones

Comando usado: `time ab -n NN http://127.0.0.1:PORT/`

Donde *NN* es el número de peticiones totales a realizar.

**Tiempo en procesar total de peticiones**

| Peticiones | NodeJS | Python |
| --- | --- | --- |
| 2000 | 0.99 seg | 2.02 seg |
| 5000 | 2.57 seg | 5.49 seg |
| 10000 | 4.81 seg | 12.85 seg |

**Peticiones por segundo**

| Peticiones | NodeJS | Python | 
| --- | --- | --- |
| 2000 | 2072 req/seg | 1005 req/seg | 
| 5000 | 1971 req/seg | 915 req/seg |
| 10000 | 2084 req/seg | 779 req/seg |

## Tiempo requerido en atender X clientes

Comando usado: `time ab -c CC -n 10000 http://127.0.0.1:PORT/`

Donde *CC* es el número de clientes concurrentes.

**NOTA IMPORTANTE 1**

    En librería `aiohttp`, el paquete `web` trae la restricción de 128 conexiones concurrentes. No se si adrede o por olvido. 

    Las pruebas han sido hechas con esta limitación y con un parché que he generado para esta librería. Dicho parche (2 lineas de código) se ha enviado al autor y se puede consultar aquí:

    https://github.com/KeepSafe/aiohttp/pull/892

**NOTA IMPORTANTE 2:**

    NodeJS viene configurado con 512 conexiones concurrentes por defecto. Si queremos soportar un mayor número de conexiones, tendremos modificar el valor *backlog* cuando invocamos a la función *listen*, de la siguiente manera:

    app.listen(PORT, backlog=5000);

    Podéis consultar la documentación oficial al respecto en:

    https://nodejs.org/api/http.html#http_server_listen_port_hostname_backlog_callback

### Ejecución con configuración por defecto

Es decir: sin el parche de Python y sin modificar la propiedad *backlog* de NodeJS.

| Clientes concurrentes | NodeJS | Python |
| --- | --- | --- |
| 100 | 3.18 seg | 9.82 seg |
| 250 | 3.10 seg | - |
| 500 | 10.75 seg |  |
| 1000 | - | - |

### Ejecución con configuración mejorada

Es decir: CON el parche de Python y con la propiedad de *backlog* de NodeJS a *5000*.

| Clientes concurrentes | NodeJS | Python |
| --- | --- | --- |
| 100 | 3.18 seg | 9.82 seg |
| 250 | 3.10 seg | 10.581 seg |
| 500 | 8.27 seg | 9.90 seg |
| 1000 | 2.89 seg | 9.77 seg |
| 4000 | - | 11.56 seg |

**Aquellas celdas donde aparece "-" (sin datos) significa que el servidor rechaza conexiones y no soporta ese flujo de información.**

# Conclusiones

Bueno... los datos son los que son. Cada cual podéis juzgar. Por la parte que me toca que quedo con lo siguiente:

**NodeJS** demuestra un **rendimiento mucho superior**, en general.

Del mismo modo resulta **curioso que NodeJS ante 4000 clientes concurrentes NO sea capaz de atenderlos** y que, **Python**, a su "chino chano" (aka poco a poco :D) **si que es capaz de atenderlos**.

Decir que no soy experto en NodeJS. Por lo que, si alguien que sepa más que yo de NodeJS (con poco) y crea que el código está mal o no del todo bien... please, comentadlo! :)

Chau!
