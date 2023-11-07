import propar

class BronkhorstPressureController():
    """
    """

    def __init__(self):
        """
        """
        raise NotImplementedError()

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
        self._logger.info(f'Connected to pressure controller. Max controlled pressure: {self._max_controlled_pressure} {self._pressure_unit}. Current setpoint value: {setpoint} {self._pressure_unit}. Current measured value: {measure} {self._pressure_unit}')

    def set_pressure(self, pressure:float):
        """
        """
        if not self._connected:
            raise WrongDeviceStateException(f'Device with S/N {self._serial_number} is not connected')
        if pressure > self._max_controlled_pressure:
            raise OutOfDeviceCapacityException(f'Trying to set pressure {pressure} {self._pressure_unit} on a device with max capacity of {self._max_controlled_pressure} {self._pressure_unit}')
        self._propar_instrument.writeParameter(dde_nr=206, data=pressure)
