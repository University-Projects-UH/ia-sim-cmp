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

## Execute

```bash
$python3 index.py code.botlang
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

## Sintaxis

El lenguaje nuestro cuenta con los tipos int, bool, float, string y date; para los números enteros, las expresiones booleanas, los números flotantes, string y fechas (el formato de estas es yyyy-mm-dd). La manera de instanciarlos es la siguiente: 

```python
int x = 5;
```

De manera análoga para el resto. También en lugar del número solamente se puede poner una expresión aritmética: 

```python
int x = 5*6 + 2;
```

También contiene una serie de operaciones para binarias y unarias: operaciones aritméticas (suma, resta, ...) y operaciones de comparación (mayor, igual, negación, ...)

Para imprimir en la consola se utiliza la funcion *print*, de la siguiente manera:

```python
print x;
print "Hola Mundo";
```

También contaremos con un conjunto de objetos específicos de nuestro lenguaje:

$\bullet$ Los bots: que pueden ser de varios tipos (smart bot, grid bot, rebalance bot) y con varias configuraciones. Mostraremos con un ejemplo como luce la sintaxis para crear los bots: 

``` python
grid_bot x = grid_bot(p1, ..., pn);
```

-El grid\_bot recibe 7 parámetros que son (en ese orden): stop\_loss take\_profit, investment, grids, limit\_low, limit\_high y assets\_array.  

-El rebalance bot recibe 6 parámetros (los dos últimos son opcionales): stop\_loss, take\_profit, investment, assets\_array.  

-El smart bot recibe 4 parámetros: stop\_loss, take\_profit, investment, assets\_array.  

$\bullet$ Los assets: son objetos que representan activos específicos. Mostraremos con dos ejemplos la sintaxis para crear activos:

```python
asset x = CreateAsset("BTC"); # para crear un solo asset
```

``` python
array assets = [CreateAsset("A1"), CreateAsset("A2"),...]; # para crear un array de asset 
```

$\bullet$ Los portfolios:

``` python
array x = PortfolioSDMin(p1, p2)
array y = PortfolioMSR(p1, p2)
```

-El portfolio recibe 2 parámetros: assets array y date.

También tendremos un conjunto de funciones propias de la lógica de los bots: 

- CreateAsset: Recibe el string con el nombre del activo y se le asocia a una variable

- PrintInfo: Imprime la información del bot, ya sea los activos con los que opera, y alguno de sus atributos.

- Run: Se usa para hacer un llamado al bot a que inicie la simulación.

- PrintHistory: Para imprimir el historial de operaciones del bot.