# PID Logic with boil threshold and .

If the target Temperature is above a configurable "Max. PID Temperature" threshold the PID will be ignored and heater is switched into boil mode. This is helpful if you use the same kettle for mashing and boiling.

In boil mode, the heater will be constantly on until the target Temperature is above a configurable "Max. Boil Temperature" threshold where the power will be reduced to the "Max. Boil Output". This is helpful to reduce power usage and avoid scortching.

## Parameter

* P - proportional value
* I - integral value
* D - derivative value
* Max. Ramp Output - heater power when above Max. PID Temperature
* Max. PID Temperature - Above this temperature the heater will be constantly on until Max. Boil Temperature is reached
* Max. Boil Output - heater power when above Max. Boil Temperature
* Max. Boil Temperature - Above this temperature the heater will use Max. Boil Output power
