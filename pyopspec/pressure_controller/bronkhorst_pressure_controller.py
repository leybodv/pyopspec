import time

import propar

from .pressure_controller import PressureController
from .exceptions import *
from .logging import get_logger

class BronkhorstPressureController(PressureController):
    """
    """

    def __init__(self, port:str, serial_number:str, logfilename:str, address:int=1):
        """
        """
        self._port = port
        self._serial_number = serial_number
        self._address = address
        self._connected = False
        self._logger = get_logger(self.__class__.__name__, logfilename=logfilename)

    def connect(self):
        """
        """
        self._propar_instrument = propar.instrument(comport=self._port, address=self._address)
        device_sn = self._propar_instrument.readParameter(92)
        if device_sn != self._serial_number:
            raise WrongDeviceException(f'Trying to connect device with S/N {self._serial_number} to the device with S/N {device_sn}')
        self._connected = True
        self._propar_instrument.wink()
        self._max_controlled_pressure = self._propar_instrument.readParameter(21)
        self._pressure_unit = self._propar_instrument.readParameter(129)
        setpoint = self._propar_instrument.readParameter(206)
        measure = self._propar_instrument.readParameter(205)
        self._logger.info(f'Connected to pressure controller {self._serial_number}. Max controlled pressure: {self._max_controlled_pressure} {self._pressure_unit}. Current setpoint value: {setpoint} {self._pressure_unit}. Current measured value: {measure} {self._pressure_unit}')

    def ramp_pressure(self, pressure:float, ramp_rate:float):
        """
        Increase/decrease pressure at a specified speed. Actual rate is not guaranteed. Program changes setpoint at the specified rate.

        params
        ------
            pressure:float
                pressure in the device units
            ramp_rate:float
                pressure increase/decrease rate in <pressure device units>/min
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        if ramp_rate > self._max_controlled_pressure * 60:
            raise OutOfDeviceCapacityException(f'Trying to raise pressure at {ramp_rate} {self._pressure_unit}/min with maximum rate {self._max_controlled_pressure * 60} {self._pressure_unit}/min')
        if pressure > self._max_controlled_pressure: #pyright: ignore[reportGeneralTypeIssues]
            raise OutOfDeviceCapacityException(f'Trying to set pressure {pressure} {self._pressure_unit} on a device with max capacity of {self._max_controlled_pressure} {self._pressure_unit}')
        measure = self._propar_instrument.readParameter(205)
        if measure > pressure: # decreasing pressure
            setpoint = measure
            while setpoint > pressure:
                setpoint = setpoint - ramp_rate / 60
                self._propar_instrument.writeParameter(dde_nr=206, data=setpoint)
                time.sleep(1)
        elif measure < pressure: # increasing pressure
            setpoint = measure
            while setpoint < pressure:
                setpoint = setpoint + ramp_rate / 60
                self._propar_instrument.writeParameter(dde_nr=206, data=setpoint)
                time.sleep(1)
        else:
            return

    def set_pressure(self, pressure:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        if pressure > self._max_controlled_pressure: #pyright: ignore[reportGeneralTypeIssues]
            raise OutOfDeviceCapacityException(f'Trying to set pressure {pressure} {self._pressure_unit} on a device with max capacity of {self._max_controlled_pressure} {self._pressure_unit}')
        self._propar_instrument.writeParameter(dde_nr=206, data=pressure)
        self._logger.info(f'Set pressure of {self._serial_number} to {pressure} {self._pressure_unit}')

    def get_pressure(self) -> float:
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        measure = self._propar_instrument.readParameter(205)
        self._logger.debug(f'Measured pressure on pressure controller {self._serial_number}: {measure} {self._pressure_unit}')
        return measure #pyright: ignore[reportGeneralTypeIssues]
