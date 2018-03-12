# PID Logic with boil threshold and boil power reduction.

If the target Temperature is above a configurable "Max. PID Temperature" threshold the PID will be ignored and heater is switched into boil mode. This is helpful if you use the same kettle for mashing and boiling.

In boil mode, the heater will be constantly on until the target Temperature is above a configurable "Max. Boil Temperature" threshold where the power will be reduced to the "Max. Boil Output". This is helpful to reduce power usage, avoid scorching and reduce boil overs.

## Parameter

* P - proportional value
* I - integral value
* D - derivative value
* Max. Output - Max power for PID and Ramp up.
* Max. PID Temperature - If Target Temperature is set above this, PID will be disabled and Boil Mode will turn on.
* Max. Boil Output - Heater power when Max Boil Temperature is reached.
* Max. Boil Temperature - When Temperature reaches this, power will be reduced to Max Boil Output.

* Internal Loop Time - In seconds, how quickly the internal loop will run, dictates maximum PID resolution (e.g. 0.1). The lower the more accurate but more demading on your Pi. You should also consider how fast your relays etc can switch when setting this.

* Mash Pump Rest Interval - In seconds, how long the pump will run during mash phase before resting.
* Mash Pump Rest Time - How long the pump will be off during the rest interval

* Pump Max Temp - The pump will be switched off and rest logic disabled after the boil reaches this temperature. If the temperature falls the pump will be switched back on but rest logic will remain disabled.
