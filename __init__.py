import logging
import time

from modules import cbpi
from modules.core.controller import KettleController
from modules.core.props import Property

@cbpi.controller
class PIDSmartBoilWithPump(KettleController):

    a_p = Property.Number("P", True, 102, description="P Value of PID")
    b_i = Property.Number("I", True, 100, description="I Value of PID")
    c_d = Property.Number("D", True, 5, description="D Value of PID")
    d_max_output = Property.Number("Max Output %", True, 100, description="Max power for PID and Ramp up.")
    e_max_temp_pid = Property.Number("Max PID Target Temperature", True, 80,description="If Target Temperature is set above this, PID will be disabled and Boil Mode will turn on.")        
    f_max_output_boil = Property.Number("Max Boil Output %", True, 70, description="Power when Max Boil Temperature is reached.")
    g_max_temp_boil = Property.Number("Max Boil Temperature", True, 98,description="When Temperature reaches this, power will be reduced to Max Boil Output.")

    h_internal_loop_time = Property.Number("Internal loop time", True, 0.2, description="In seconds, how quickly the internal loop will run, dictates maximum PID resolution.")

    j_mash_pump_rest_interval = Property.Number("Mash pump rest interval", True, 600, description="Rest the pump after this many seconds during the mash.")

    j_mash_pump_rest_time = Property.Number("Mash pump rest time", True, 60, description="Rest the pump for this many seconds every rest interval.")

    def __init__(self, *args, **kwds):
        KettleController.__init__(self, *args, **kwds)
        self._logger = logging.getLogger(type(self).__name__)

    def stop(self):
        '''
        Invoked when the automatic is stopped.
        Normally you switch off the actors and clean up everything
        :return: None
        '''
        super(KettleController, self).stop()
        self.heater_off()


    def run(self):
        wait_time = sampleTime = 5
        p = float(self.a_p)
        i = float(self.b_i)
        d = float(self.c_d)
        
        maxoutput = float(self.d_max_output)          
        maxtemppid = float(self.e_max_temp_pid)
        
        pid = PIDArduino(sampleTime, p, i, d, 0, maxoutput)
        
        maxoutputboil = float(self.f_max_output_boil)
        maxtempboil = float(self.g_max_temp_boil)

        if maxtempboil > maxoutput:
            raise ValueError('maxtempboil must be less than maxoutput')

        self.start_time = time.time()
        internal_loop_time = float(self.h_internal_loop_time)
        self._logger.debug(self.h_internal_loop_time)
        self._logger.debug(internal_loop_time)

        mash_pump_rest_interval = int(self.j_mash_pump_rest_interval)
        mash_pump_rest_time = int(self.j_mash_pump_rest_time)

        next_pump_start = now
        next_pump_rest = None

        while self.is_running():
            self._logger.debug("calculation cycle")
            inner_loop_now = calculation_loop_start = time.time()
            next_calculation_time = calculation_loop_start + sampleTime
            target_temp = self.get_target_temp()
            current_temp = self.get_temp()
            boil_mode = target_temp > maxtemppid

            if not boil_mode: #PID
                heat_percent = pid.calc(current_temp, target_temp)
            elif current_temp < maxtempboil: #Boil Ramp
                heat_percent = maxoutput
            else: #Boil Sustain
                heat_percent = maxoutputboil
                
            heating_time = sampleTime * heat_percent / 100
            heat_to = calculation_loop_start + heating_time

            wait_time = sampleTime - heating_time

            while inner_loop_now < next_calculation_time:
                self._logger.debug("inner loop cycle")

                if inner_loop_now == calculation_loop_start and heating_time > 0:
                    self._logger.debug("inner loop heat on")
                    self.heater_on(100)

                if inner_loop_now > calculation_loop_start and \
                        inner_loop_now >= heat_to and \
                        wait_time > 0:
                    self._logger.debug("inner loop heat off")
                    self.heater_off()
                    wait_time = -1  # to stop off being called continuously

                if next_pump_start and inner_loop_now >= next_pump_start:
                    self._logger.debug("starting pump")
                    next_pump_start = None
                    next_pump_rest = inner_loop_now + mash_pump_rest_interval
                elif next_pump_rest and inner_loop_now >= next_pump_rest:
                    self._logger.debug("resting pump")
                    next_pump_rest = None
                    next_pump_start = inner_loop_now + mash_pump_rest_time

                self.sleep(internal_loop_time)
                inner_loop_now = time.time()

# Based on Arduino PID Library
# See https://github.com/br3ttb/Arduino-PID-Library
class PIDArduino(object):

    def __init__(self, sampleTimeSec, kp, ki, kd, outputMin=float('-inf'),
                 outputMax=float('inf'), getTimeMs=None):
        if kp is None:
            raise ValueError('kp must be specified')
        if ki is None:
            raise ValueError('ki must be specified')
        if kd is None:
            raise ValueError('kd must be specified')
        if sampleTimeSec <= 0:
            raise ValueError('sampleTimeSec must be greater than 0')
        if outputMin >= outputMax:
            raise ValueError('outputMin must be less than outputMax')

        self._logger = logging.getLogger(type(self).__name__)
        self._Kp = kp
        self._Ki = ki * sampleTimeSec
        self._Kd = kd / sampleTimeSec
        self._sampleTime = sampleTimeSec * 1000
        self._outputMin = outputMin
        self._outputMax = outputMax
        self._iTerm = 0
        self._lastInput = 0
        self._lastOutput = 0
        self._lastCalc = 0

        if getTimeMs is None:
            self._getTimeMs = self._currentTimeMs
        else:
            self._getTimeMs = getTimeMs

    def calc(self, inputValue, setpoint):
        now = self._getTimeMs()

        if (now - self._lastCalc) < self._sampleTime:
            return self._lastOutput

        # Compute all the working error variables
        error = setpoint - inputValue
        dInput = inputValue - self._lastInput

        # In order to prevent windup, only integrate if the process is not saturated
        if self._lastOutput < self._outputMax and self._lastOutput > self._outputMin:
            self._iTerm += self._Ki * error
            self._iTerm = min(self._iTerm, self._outputMax)
            self._iTerm = max(self._iTerm, self._outputMin)

        p = self._Kp * error
        i = self._iTerm
        d = -(self._Kd * dInput)

        # Compute PID Output
        self._lastOutput = p + i + d
        self._lastOutput = min(self._lastOutput, self._outputMax)
        self._lastOutput = max(self._lastOutput, self._outputMin)

        # Log some debug info
        self._logger.debug('P: {0}'.format(p))
        self._logger.debug('I: {0}'.format(i))
        self._logger.debug('D: {0}'.format(d))
        self._logger.debug('output: {0}'.format(self._lastOutput))

        # Remember some variables for next time
        self._lastInput = inputValue
        self._lastCalc = now
        return self._lastOutput

    def _currentTimeMs(self):
        return time.time() * 1000
