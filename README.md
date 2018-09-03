# PID Logic with Boil and Pump control

Forked from [PID Smart Boil](https://github.com/TChilderhose/cbpi-pidsmartboil) by [TChilderhose](https://github.com/TChilderhose) and extended to be able to pulse the pump during the mash phase.

These modifications have been made so that CraftBeerPi3 would be better able to control single vessel breweries with integrated pumps.

## Mash and boil in single vessel

If the target Temperature is above a configurable `Max. PID Temperature` threshold the PID will be ignored and heater is switched into boil mode. This is helpful if you use the same kettle for mashing and boiling.

In boil mode, the heater will be constantly on until the target Temperature is above a configurable `Max. Boil Temperature` threshold where the power will be reduced to the `Max. Boil Output`. This is helpful to reduce power usage, avoid scorching and reduce boil overs.

## Automatic Pump Control

While the temperature is below `Pump Max Temp`, the pump will be run for `Mash Pump Rest Interval` seconds, then switched off for `Mash Pump Rest Time` seconds, and then the cycle will repeat.

Once the temperature reaches or exceeds `Pump Max Temp` the pump will be switched off.

### Pre-starting Hot-Side Cooling Loop

You may wish to run the pump before the end of the boil (e.g. to sanitize a plate-chiller or counterflow chiller) but `Pump Max Temp` will prevent you.

You can get around this by:

* having a physical SPDT mode switch between your logic board and the pump's relay, allowing you to manually force the pump on; or

* having an _or gate_ or a _second transistor_ between a spare GPIO pin and the pump's relay, and then having an override toggle on your CraftBeerPi dashboard

## Parameters

* `P` - proportional value
* `I` - integral value
* `D` - derivative value
* `Max. Output` - Max power for PID and Ramp up.
* `Max. PID Temperature` - If Target Temperature is set above this, PID will be disabled and Boil Mode will turn on.
* `Max. Boil Output` - Heater power when Max Boil Temperature is reached.
* `Max. Boil Temperature` - When Temperature reaches this, power will be reduced to Max Boil Output.

* `Internal Loop Time` - In seconds, how quickly the internal loop will run, dictates maximum PID resolution (e.g. 0.1). The lower the more accurate but more demanding on your Pi. You should also consider how fast your relays etc can switch when setting this.

* `Mash Pump Rest Interval` - In seconds, how long the pump will run during mash phase before resting.
* `Mash Pump Rest Time` - How long the pump will be off during the rest interval

* `Pump Max Temp` - The pump will be switched off and rest logic disabled after the boil reaches this temperature. If the temperature falls the pump will be switched back on but rest logic will remain disabled.
