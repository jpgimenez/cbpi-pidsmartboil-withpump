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
