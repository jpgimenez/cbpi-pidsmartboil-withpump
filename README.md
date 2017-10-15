# PID Logic with boil threshold and boil power reduction.

If the target Temperature is above a configurable "Max. PID Temperature" threshold the PID will be ignored and heater is switched into boil mode. This is helpful if you use the same kettle for mashing and boiling.

In boil mode, the heater will be constantly on until the target Temperature is above a configurable "Max. Boil Temperature" threshold where the power will be reduced to the "Max. Boil Output". This is helpful to reduce power usage and avoid scortching.

## Parameter

* P - proportional value
* I - integral value
* D - derivative value
* Max. Output - max heater power using PID or ramping up for boil
* Max. PID Temperature - Above this target temperature the heater will quickly as possible reach Max. Boil Temperature
* Max. Boil Output - heater power when Max. Boil Temperature is reached
* Max. Boil Temperature - At or above this temperature and the heater will use Max. Boil Output power
