# ia-simp-cmp Assets Bots simulator

## Integrantes:
- Alben Luis Urquiza Rojas C312
- Frank Abel Blanco Gómez C312
- Karel Díaz Vergara C312

## Install and run
``` bash
$ git clone https://github.com/University-Projects-UH/ia-sim-cmp
$ cd ./ia-sim-cmp
$ python3 -m virtualenv env
$ source env/bin/activate
$ pip3 install < requirements.txt
```

## Run tests:
``` bash
$ pytest
```

## Resumen:

Existen dos entidades fundamentales, los activos y los bots, de forma tal que con el lenguaje puedas crear activos y asociarle una gráfica de yahoo finance, esto para poder tener un histórico de este activo, y poder simular la corrida de los bots.
Luego tenemos los bots, la idea fundamental de estos es simular operaciones en el mercado de compras y ventas para maximizar el profit, tenemos la idea de crear un bot de rebalance, que trabaja con varios activos, otro bot que sea más inteligente, otro llamado grid bot que viene siendo más de simulación, pero la idea en general es que puedas ajustarle parámetros a estos, ya sea el rango en el que van a correr de tiempo y de precio, take profits de cada operación y en general, así mismo como stop loss, etc etc, además de ponerle parámetros para que los bots tengan en cuenta algunos análisis de mercado, como lo es análisis de media móvil, resistencia, soportes y otros indicadores.

Bots disponibles:
- Grid Bot
- Smart Bot
- Rebalance Bot
